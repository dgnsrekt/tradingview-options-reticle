from options_reticle.ticker import TickerData


def test_parse_from_tv_ticker_id():
    ticker_one = TickerData(symbol="AAPL", exchange="NASDAQ")
    ticker_two = TickerData.parse_from_tv_ticker_id("NASDAQ:AAPL")
    assert ticker_one == ticker_two

    for ticker in [ticker_one, ticker_two]:
        assert ticker.expiration == None
        assert ticker.last_price == None
