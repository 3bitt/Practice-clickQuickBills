import click
import json
import functions
from functions import calculateBill

@click.group()
def bills():
    pass


@bills.command('show')
@click.option('--month', '-m', help='Show specific month [YYYY/MM]')
@click.option('--all', is_flag=True, help='Show all months')
def show(all, month):
    """
    Print meter states, args: --all, -m [YYYY/MM]
    """
    with open('bills_history.json', 'r') as read:
        loaded_dict = json.load(read)

        if all:
            print(json.dumps(loaded_dict, sort_keys=True, indent=3))
        elif month:
            print(json.dumps(loaded_dict[month], indent=3))
    read.close()


@bills.command('new')
def addNewBill():
    """
    Start adding new bill
    """
    period = click.prompt('Provide year and month of bill [YYYY/MM] ', type=str)
    while not functions.check_period_format(period):
        period = click.prompt('Provide year and month of bill [YYYY/MM] ', type=str)

    electricityMeterState = click.prompt(
        click.style('Electricity ', fg='cyan', bold=True) + 'current meter state [xx.yy] ', type=float)
    waterMeterState = click.prompt(
        click.style('Water ', fg='blue', bold=True) + 'current meter state [xx.yy] ', type=float)
    gasMeterState = click.prompt(
        click.style('Gas ', fg='bright_white', bold=True) + 'current meter state [xx.yy] ', type=float)

    with open('bills_history.json', 'r') as read:
        # If something in file then append to dictionary
        if read.read():
            read.seek(0)
            loaded_dict = json.load(read)
            # Check if given month already exists in json file
            if period in loaded_dict:
                click.secho(f'Error: Month {period} already exists ! - Exiting', fg='red')
                exit(0)

            loaded_dict[period] = {'meterStates': {
                'electricityMeterState': electricityMeterState,
                'waterMeterState': waterMeterState,
                'gasMeterState': gasMeterState
            }
            }
            # Magic calculations
            modifiedDict = calculateBill(loaded_dict)

            # Save dictionary to file
            with open('bills_history.json', 'w') as write:
                json.dump(modifiedDict, write)
                write.close()

        # If file is empty then create new dictionary
        else:
            loaded_dict = {
                period: {'meterStates': {
                    'electricityMeterState': electricityMeterState,
                    'waterMeterState': waterMeterState,
                    'gasMeterState': gasMeterState
                }
                }
            }
            # Save dictionary to file
            with open('bills_history.json', 'w') as write:
                json.dump(loaded_dict, write)
                write.close()
    read.close()
    click.secho('\n--- Saved! ---\n', fg='green', bold=True)

if __name__ == '__main__':
    bills()
