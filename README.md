
![alt text](images/options_reticle_v4.png)

<!-- # [FDD] **Options Reticle** -->
# ***[FDD] Options Reticle caters to degenerate traders and gamblers worldwide, reaching out for long distant contract expiration and just OTM strike placement.***

## 🍾🍾 **Congratulations on your choice of Options Reticle.** 🎉🎉

### The Options Reticle provides a targeting system overlay that will show a horizontal OTM strike price and verticle expiration target. If you're thinking as soon as the expiration date has passed, this overlay will be useless; you're right but, you can use the `options-reticle` CLI tool to generate a new overlay from a watchlist exported from TradingView.


## Install with [pipx](https://github.com/pipxproject/pipx)

```bash
$ pipx install options-reticle
```
### [>> WATCH THE SCRIPT RUN HERE <<](https://asciinema.org/a/366342)

![alt text](images/aapl_basic.gif)

[![alt text](https://www.tradingview.com/x/U95ddn6i/)](https://www.tradingview.com/x/U95ddn6i/)

[![alt text](https://www.tradingview.com/x/bjJedDvF/)](https://www.tradingview.com/x/bjJedDvF/)

[![alt text](https://www.tradingview.com/x/c1Md17a8/)](https://www.tradingview.com/x/c1Md17a8/)

[![alt text](https://www.tradingview.com/x/cLFQzQFW/)](https://www.tradingview.com/x/cLFQzQFW/)


## OVERLAY FEATURES:
* `Quick Action PUT (QAP) Mode` - When you flip the chart by adding a 0- in front of the symbol, you will see the PUT contract target.
* `Strike Price / Expiration Crosshairs`.
* `Fill Mode` - Shows a fill between the historical price and the target strike price. It will show green when ITM and red when OTM.
* `Target information panel` - Shows the company name, days till expiration, month and day of expiration, strike price, dollars OTM or ITM, and the contract type.
* `Emotion Indicator` - Shows an exact representation of your feelings based on if you were in the trade. It has an accuracy of 99.9 percent.

## QUICK ACTION PUT (QAP) MODE:
This style of reticle is not visible until you flip the chart. The advantage of the (QAP) is that it maintains the same appearance as the standard style of reticle, making PUT contract targeting feel the same. When targeting with (QAP) mode, be aware that the chart prices are reversed. Up is down, and down is up; this can be confusing but will feel normal overtime. Activate QAP mode by appending a `0-` to the symbol of the chart. If nothing appears, no put option data was found for that symbol.

[![alt text](https://www.tradingview.com/x/z9Uqdo2h/)](https://www.tradingview.com/x/z9Uqdo2h/)

## CALIBRATING YOUR RETICLE
The overlay is generated using the options-reticle CLI tool found on GitHub. The adjustment script will parse a watchlist exported from TradingView then download options data for each ticker in the watchlist. The max amount of symbols you can add to a single overlay is about 200. Any more than 200 and the overlay will crash. Luckily, If you use a TradingView watchlist with more than 200 ticker symbols to generate overlays, the options-reticle command-line tool will automatically create multiple overlays with 200 tickers each. You can add multiple overlays to your chart to get all the tickers in the watchlist.

## RETICLE GENERATION AND MOUNTING:
1. Add all the tickers you want to track into a watchlist on Tradingview.
2. Export the watchlist into a txt file using TradingView's watchlist export list button.
3. Open the terminal and change to the directory with the downloaded watchlist txt file.
4. Install options-reticle command tool with pipx. pipx install tradingview-options-reticle.
5. Run the command options-reticle download --watchlist {name of watchlist.txt file}. This will download the options data to an options_data.toml in the same directory as the watchlist txt file.
6. Run the command options-reticle build --options-data-input-path options_data.toml. This will generate the overlay scripts. If the watch list has more than 200 ticker symbols, it will generate a separate overlay script for every 200 ticker symbol chunk.
7. Copy and paste each of the generated overlay scripts one at a time into the Pine Editor on TradingView, then click the Add to Chart button. Make sure you copy the entire code.

### EXAMPLE OF RETICLE GENERATION
[![asciicast](https://asciinema.org/a/366342.png)](https://asciinema.org/a/366342)

## FUTURE FEATURES:
* Give the choice to generate PUT option contracts without using QAP mode. This option will allow you to use the input settings to change the contract type without flipping the chart.
* Max OTM target argument - This will allow the option-reticle CLI to generate overlays with deeper OTM contracts. It currently only searches for the first OTM contract.
* Add the ability to change the crosshair line type. [dash, dotted, solid]

## TODO
* [ ] More Testing.
* [ ] More Features.
* [ ] More Docs.

## Contact Information
Telegram = Twitter = Tradingview = Discord = @dgnsrekt

Email = dgnsrekt@pm.me
