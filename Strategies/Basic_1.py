config = {
    "GeneralConfig" : {
        "name" : "Basic_Config_1",
        "buy_threshold": 0,
        "sell_threshold": 0,
        "interval": "15m",
        "period": "1mo"
    },

    "IndicatorConfig" : {
        "requiredDataLength": 10,
        "field" : "close",
        "EMA": [13, 52],
        "RSI": 14,
        "MACD": {'fast':12,'slow':26,'signal':9},
    },

    "EntryConfig" : {
        "conditions": [
            {"type":"rangePlus", "field1": "EMA13", "field2": "EMA52", "period": 3, "color": 0, "score": 1},
        ],
        "indicators": [
            # {"type":"lastCrossOver", "field1": "close", "field2": "52wh", "period": 13, "color": 3, "score": 6},
            {"type":"rangePlus", "field1": "RSI", "field2": 50, "period": 5, "color": 3, "score": 4},
        ],
        "confirmations": [
            {'type':'rising','field':'macd_histogram','period':3,'color':2,'score':4},
            {'type':'rising','field':'RSI','period':3, 'color':2, 'score':2},
            {"type":"rising", "field": "EMA13","period": 3, "color": 2, "score": 2},
        ]
    },
    
    "ExitConfig" : {
        "conditions": [
            {"type":"rangeMinus", "field1": "EMA13", "field2": "EMA52", "period": 3, "color": 0, "score": 1},
        ],
        "indicators": [
            # {"type":"lastCrossOver", "field1": "close", "field2": "52wl", "period": 13, "color": -3, "score": 6},
            {"type":"rangeMinus", "field1": "RSI", "field2": 50, "period": 5, "color": -3, "score": 4},
        ],
        "confirmations": [
            {'type':'falling','field':'macd_histogram','period':3,'color':-2,'score':4},
            {'type':'falling','field':'RSI','period':3, 'color':-2, 'score':2},
            {"type":"falling", "field": "EMA13","period": 3, "color": -2, "score": 2},
        ]
    }
}