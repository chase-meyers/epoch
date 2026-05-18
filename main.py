import rich
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich import print
from rich.table import Table
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
    console = Console()
    regime_names = {0: 'High Volatility', 1: 'Sideways/Neutral', 2: 'Crisis/Bear', 3: 'Bull/Trending'}

    if data is None:
        print("Could not fetch data. Exiting.")

    else:
        engineered_data = engineer_features(data)
        train_model, scaler = train(engineered_data)
        regimes, probabilities = predict(train_model, scaler, engineered_data)
        regime = regimes[-1]

        grouping_df, validation_df = validate(engineered_data, regimes)


        display_df = grouping_df.reset_index()

        console.print()
        console.print()

        table = Table(title=f"Regime Characteristics for {ticker}", show_lines=True)
        for col in display_df.columns:
            table.add_column(col)
        for _, row in display_df.iterrows():
            values = [interpret(int(row['regime']))] + [f"{val:.4f}" for val in row[1:]]
            table.add_row(*values)
        
        console.print(f"Latest Regime: {interpret(regime)}", justify="center", style="bold")

        console.print()

        # Confidence Probabilities
        conf_table = Table(show_header=False, box=None, padding=(0, 2))
        conf_table.add_column(justify="right", style="white")
        conf_table.add_column(justify="left")
        conf_table.add_column(justify="left", style="cyan")

        for i, prob in enumerate(probabilities[-1]):
            bar_length = int(prob * 20)
            bar = '█' * bar_length + '░' * (20 - bar_length)
            conf_table.add_row(regime_names[i], bar, f"{prob*100:.1f}%")

        console.print(conf_table, justify="center")

        console.print()
        console.print()

        console.print(table, justify="center", style="bold")


        generate_charts(data, validation_df)

if __name__ == "__main__":    main()