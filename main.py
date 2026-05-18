import rich
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich import print
from data.fetcher import fetch_data
from features.engineer import engineer_features
from models.regime import train, predict, interpret
from validation.validator import validate, generate_charts

def display_welcome():
    console = Console()

    console.print()
    console.print()
    console.print()
    console.print()

    title = pyfiglet.figlet_format("E P O C H", font="ansi_shadow")
    console.print(title, style="bold white", justify="center")

    console.print("M A R K E T  R E G I M E  A N A L Y S I S  E N G I N E", style="dim white", justify="center")

def get_ticker_input():
    console = Console()

    console.print()
    console.print()
    console.print()
    console.print()
    console.print()
    console.print()

    ticker = input("Ticker (default: SPY): ").strip().upper()
    if not ticker:
        ticker = "SPY"
    return ticker

def main():
    display_welcome()
    ticker = get_ticker_input()
    data = fetch_data(ticker)

    if data is None:
        print("Could not fetch data. Exiting.")

    else:
        engineered_data = engineer_features(data)
        print( engineered_data )
        train_model, scaler = train(engineered_data)
        regimes, probabilities = predict(train_model, scaler, engineered_data)
        regime = regimes[-1]
        print(f"Current Regime: {interpret(regime)}, Probabilities = {probabilities[-1]}")

        grouping_df, validation_df = validate(engineered_data, regimes)
        print(grouping_df)
        generate_charts(data, validation_df)

if __name__ == "__main__":    main()