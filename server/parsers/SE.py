import arrow
import requests

COUNTRY_CODE = 'SE'

def fetch_SE():
    url = 'http://driftsdata.statnett.no/restapi/ProductionConsumption/GetLatestDetailedOverview?timestamp={}'.format(arrow.now().timestamp * 1000)

    data = requests.get(url).json()
    countries = map(lambda x: x['value'], data['Headers'])
    i = countries.index(COUNTRY_CODE)

    obj = {
        'countryCode': COUNTRY_CODE,
        'datetime': arrow.get(arrow.get(data['MeasuredAt'] / 1000).datetime, 
            'Europe/Stockholm').datetime
    }
    obj['consumption'] = {
        'other': float(data['ConsumptionData'][i]['value'].replace(u'\xa0', '').replace(' ', '').replace('-', '0'))
    }
    obj['exchange'] = {
    }
    obj['production'] = {
        'other': float(data['ThermalData'][i]['value'].replace(u'\xa0', '').replace(' ', '').replace('-', '0')) + 
            float(data['NotSpecifiedData'][i]['value'].replace(u'\xa0', '').replace(' ', '').replace('-', '0')),
        'wind': float(data['WindData'][i]['value'].replace(u'\xa0', '').replace(' ', '').replace('-', '0')),
        'nuclear': float(data['NuclearData'][i]['value'].replace(u'\xa0', '').replace(' ', '').replace('-', '0')),
        'hydro': float(data['HydroData'][i]['value'].replace(u'\xa0', '').replace(' ', '').replace('-', '0')),
    }

    return obj

fetch_SE()
