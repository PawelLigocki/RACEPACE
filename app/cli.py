import argparse
from app.pace import pace_from_time, time_from_pace
from app.predictor import riegel_predict


def main():
    parser = argparse.ArgumentParser(description="Race calculator CLI")

    subparsers = parser.add_subparsers(dest="command")

    # pace command
    pace_parser = subparsers.add_parser("pace")
    pace_parser.add_argument("--distance", type=float, required=True)
    pace_parser.add_argument("--time", type=float, required=True)

    # predict command
    predict_parser = subparsers.add_parser("predict")
    predict_parser.add_argument("--distance", type=float, required=True)
    predict_parser.add_argument("--time", type=float, required=True)
    predict_parser.add_argument("--target", type=float, required=True)

    args = parser.parse_args()

    if args.command == "pace":
        pace = pace_from_time(args.distance, args.time)
        print(f"Pace: {pace:.2f} min/km (~{pace*60:.0f} sec/km)")

    elif args.command == "predict":
        result = riegel_predict(args.distance, args.time, args.target)
        print(f"Predicted time: {result:.2f} minutes")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()


