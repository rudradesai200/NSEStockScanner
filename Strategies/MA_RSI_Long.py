config = {
    "GeneralConfig" : {
        "name" : "MA_RSI_Long",
        "buy_threshold": 2,
        "sell_threshold": 2,
        "type": "long",
        "interval": "15m",
        "period": "60d"
    },

    "IndicatorConfig" : {
        "requiredDataLength": 10,
        "field" : "close",
        "EMA": [13, 52],
        "SMA": [200],
        "RSI": 14,
    },

    "EntryConfig" : {
        "indicators": [
            {"type":"crossedFromBelow", "field1": "EMA13", "field2": "EMA52", "period": 5, "color": 2, "score": 2},
            [{'type':'comparePlus','field1':'RSI','field2':60, 'color':2,'score':1},
            {'type':'rising', 'field':'RSI', 'period': 3,'color':2,'score':1}],
        ],
        "confirmations": [
            {"type":"crossedFromBelow", "field1": "RSI", "field2": 60, "period": 5, "color": 3, "score": 5},
            {'type':'crossedFromBelow','field1':'close','field2':'SMA200', "period": 5, 'color':3,'score': 5},
        ]
    },

    "ExitConfig" : {
        "indicators": [
            [{"type":"falling", "field":"close", "period": 3, "color": -2,"score":1},
            {"type":"crossedFromAbove", "field1": "RSI", "field2": 60, "period": 5, "color": -2, "score": 1}],
            {"type":"crossedFromAbove", "field1": "close", "field2": "EMA13", "period": 3, "color": -2, "score": 1}
        ],
        "confirmations": [
            {"type":"crossedFromAbove", "field1": "RSI", "field2": 40, "period": 3, "color": -3, "score": 5},
        ]
    }
}