import re
import click
import operator

def calculateResourceConsumption(new_val, old_val):
    result = float(format(new_val - old_val, '.3f'))
    return result

def calculateMeterFee(meterConsumption, meterType):
    water_factor = 9.85
    gas_factor = 1.71
    electricity_factor = 0.53
    if meterType == 'electricity':
        return float(format(meterConsumption * electricity_factor, '.2f'))
    elif meterType == 'water':
        return float(format(meterConsumption * water_factor, '.2f'))
    elif meterType == 'gas':
        return float(format(meterConsumption * gas_factor, '.2f'))
    else:
        print(click.style(f'Calculating fee amount for {meterType} is not possible!', fg='red'))
        exit(0)

def calculateTotalFee(feeDict):
    totalFee = format(sum(list(feeDict.values())), '.2f')
    return float(totalFee)


def check_period_format(period_string):
    '''
    Validate if user provided valid period (YYYY/MM)
    '''
    pattern = re.compile(r'\d{4}/\d{2}$')
    res = re.match(pattern, period_string)
    if res:
        return True
    else:
        print(click.style('Incorrect format! - should be: YYYY/MM', fg='red'))
        return False


def calculateBill(masterDict):
    """
        Take last and before-last month meter states and calculate resource consumption.
        Basing on that consumption calculate fee amount for each meter in last month.
        Save values in 2 dictionaries and add them to masterDict[lastMonth].
        Return masterDict.
    """
    consumptionDict = {}
    feeDict = {}
    # Regexp to extract meter type (prefix) from words like 'waterMeterValue' (water)
    meterNameRegex = re.compile(r'^[a-z]*')
    # Sort dictionary basing on months (asc)
    sorted_dict = dict(sorted(masterDict.items(), key=operator.itemgetter(0)))
    # Save last and before-last months identifiers (ex. 2017/09)
    dictLastItem = list(sorted_dict.keys())[-1]
    dictPenultimateItem = list(sorted_dict.keys())[-2]

    for i in range(0,3):
        # Go thru 3 meter types in for loop - each time calculate next meter consumption and fee.
        # Add results to dictionaries (consumption and fee Dicts) and at the end add these to masterDict
        itemConsumed = re.match(meterNameRegex, list(dict(sorted_dict[dictLastItem]['meterStates']))[i])

        val1 = list(dict(sorted_dict[dictLastItem]['meterStates']).values())[i]
        val2 = list(dict(sorted_dict[dictPenultimateItem]['meterStates']).values())[i]
        meterConsumption = calculateResourceConsumption(val1, val2)

        consumptionDict[itemConsumed.group()] = meterConsumption
        feeDict[itemConsumed.group()+'FeeAmt'] = calculateMeterFee(meterConsumption, itemConsumed.group())


    # Calculate and append totals to feeDict
    feeDict['total'] = calculateTotalFee(feeDict)

    sorted_dict[dictLastItem]['consumption'] = consumptionDict
    sorted_dict[dictLastItem]['fee'] = feeDict

    return sorted_dict