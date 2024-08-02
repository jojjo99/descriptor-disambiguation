import re
import matplotlib
import numpy as np

matplotlib.use("Agg")
from matplotlib.pylab import plt


aachen = {
    "gaussian": {
        "salad": {
            0.1: "17.0 / 28.6 / 60.8	4.2 / 11.5 / 35.6",
            0.2: "16.9 / 28.5 / 60.9	4.2 / 11.0 / 35.6",
            0.3: "19.7 / 30.6 / 61.8	5.2 / 12.0 / 35.6",
            0.4: "42.7 / 54.7 / 73.2	14.1 / 22.5 / 46.6",
            0.5: "73.8 / 82.2 / 91.9	52.9 / 68.6 / 84.8",
            0.6: "84.6 / 90.3 / 96.7	69.1 / 84.8 / 94.8",
            0.7: "86.4 / 92.0 / 96.8	72.3 / 85.3 / 92.1",
            0.8: "85.2 / 90.7 / 95.5	67.5 / 80.6 / 88.0",
            0.9: "84.5 / 89.9 / 95.1	64.4 / 74.9 / 81.7",
            1.0: "84.0 / 89.2 / 94.8	61.3 / 71.7 / 80.6",
        },
    },
    "random-0": {
        "salad": {
            0.1: "20.4 / 31.1 / 62.5	5.2 / 11.5 / 36.1",
            0.2: "76.6 / 83.7 / 91.9	53.9 / 73.3 / 84.3",
            0.3: "86.3 / 91.5 / 97.3	69.6 / 85.9 / 93.7",
            0.4: "85.9 / 91.5 / 96.5	70.7 / 84.8 / 90.1",
            0.5: "84.5 / 90.5 / 95.9	67.0 / 78.5 / 85.9",
            0.6: "83.7 / 89.7 / 94.8	64.9 / 76.4 / 83.2",
            0.7: "84.3 / 89.9 / 94.7	62.3 / 72.8 / 82.2",
            0.8: "84.2 / 89.4 / 94.5	62.8 / 73.8 / 81.7",
            0.9: "84.2 / 89.6 / 94.7	61.3 / 72.8 / 81.7",
            1.0: "84.0 / 89.2 / 94.8	61.3 / 71.7 / 80.6",
        },
    },
    "first": {
        "salad": {
            0.1: "27.3 / 39.4 / 66.3	8.9 / 14.1 / 37.7",
            0.2: "79.5 / 87.4 / 95.1	61.8 / 79.1 / 89.5",
            0.3: "86.9 / 92.0 / 96.8	70.2 / 84.8 / 92.7",
            0.4: "86.5 / 91.7 / 96.4	70.2 / 83.2 / 91.6",
            0.5: "84.8 / 90.2 / 96.0	67.5 / 79.1 / 86.9",
            0.6: "84.1 / 89.6 / 95.0	65.4 / 75.9 / 85.3",
            0.7: "84.1 / 89.6 / 95.0	65.4 / 75.9 / 85.3",
            0.8: "84.3 / 89.8 / 94.8	61.8 / 72.8 / 81.7",
            0.9: "84.2 / 89.4 / 94.7	60.7 / 71.2 / 80.6",
            1.0: "84.0 / 89.2 / 94.8	61.3 / 71.7 / 80.6",
        },
    },
    "last": {
        "salad": {
            0.1: "20.4 / 32.0 / 62.3	4.7 / 12.0 / 36.6",
            0.2: "74.8 / 83.3 / 91.4	51.8 / 67.0 / 81.7",
            0.3: "85.7 / 91.1 / 96.6	69.6 / 84.8 / 93.2",
            0.4: "85.4 / 90.8 / 96.0	70.7 / 82.7 / 90.1",
            0.5: "84.5 / 90.5 / 95.5	67.0 / 80.1 / 88.5",
            0.6: "84.6 / 89.8 / 94.8	63.9 / 75.4 / 85.3",
            0.7: "84.3 / 89.3 / 94.7	61.8 / 73.3 / 81.7",
            0.8: "84.0 / 89.4 / 94.7	60.7 / 72.3 / 82.2",
            0.9: "84.5 / 89.6 / 94.7	61.8 / 72.8 / 81.7",
            1.0: "84.0 / 89.2 / 94.8	61.3 / 71.7 / 80.6",
        },
    },
    "center": {
        "salad": {
            0.1: "19.9 / 31.2 / 61.9	5.2 / 12.0 / 35.6",
            0.2: "75.8 / 83.7 / 92.8	56.0 / 72.8 / 83.2",
            0.3: "85.6 / 91.6 / 97.2	69.6 / 85.3 / 93.2",
            0.4: "86.4 / 91.5 / 96.5	70.7 / 83.2 / 90.6",
            0.5: "84.5 / 90.3 / 95.0	66.5 / 79.1 / 88.0",
            0.6: "84.0 / 89.4 / 94.5	64.4 / 76.4 / 85.3",
            0.7: "83.3 / 88.8 / 94.4	61.8 / 73.3 / 83.2",
            0.8: "84.0 / 89.4 / 94.3	61.3 / 71.7 / 82.2",
            0.9: "84.2 / 89.4 / 94.1	61.3 / 71.7 / 80.1",
            1.0: "84.0 / 89.2 / 94.8	61.3 / 71.7 / 80.6",
        },
    },
}


robotcar = {
    "gaussian": {
        "salad": {
            0.1: "22.5 / 58.0 / 97.8	3.0 / 13.5 / 54.5",
            0.2: "23.3 / 57.5 / 98.1	3.0 / 13.1 / 54.5",
            0.3: "42.6 / 77.0 / 98.8	4.2 / 14.9 / 55.9",
            0.4: "57.6 / 92.4 / 99.9	14.9 / 43.8 / 88.6",
            0.5: "60.3 / 93.1 / 100.0	26.3 / 69.5 / 94.2",
            0.6: "61.2 / 93.2 / 100.0	29.8 / 79.3 / 98.1",
            0.7: "61.4 / 93.8 / 100.0	31.5 / 77.6 / 99.1",
            0.8: "61.0 / 93.9 / 100.0	24.5 / 60.4 / 86.9",
            0.9: "60.3 / 94.0 / 100.0	14.9 / 38.5 / 57.6",
            1.0: "60.8 / 93.8 / 99.9	11.9 / 33.6 / 49.7",
        },
    },
    "random-0": {
        "salad": {
            0.1: "46.4 / 82.2 / 99.3	4.2 / 15.9 / 57.8",
            0.2: "60.8 / 93.1 / 100.0	26.6 / 69.9 / 94.6",
            0.3: "61.1 / 93.1 / 100.0	32.9 / 80.9 / 99.1",
            0.4: "61.3 / 93.6 / 100.0	30.1 / 74.6 / 98.6",
            0.5: "61.6 / 94.0 / 100.0	22.4 / 58.5 / 86.0",
            0.6: "60.8 / 94.0 / 100.0	15.4 / 42.0 / 65.7",
            0.7: "60.9 / 93.7 / 100.0	14.0 / 37.1 / 53.6",
            0.8: "60.8 / 93.8 / 99.9	12.1 / 34.0 / 51.5",
            0.9: "60.8 / 93.7 / 99.9	12.8 / 33.1 / 49.2",
            1.0: "60.8 / 93.8 / 99.9	11.9 / 33.6 / 49.7",
        },
    },
    "first": {
        "salad": {
            0.1: "53.2 / 88.2 / 99.6	7.5 / 26.1 / 70.4",
            0.2: "60.6 / 93.2 / 100.0	29.4 / 73.0 / 95.8",
            0.3: "61.1 / 93.7 / 100.0	27.3 / 79.7 / 99.1",
            0.4: "61.3 / 93.9 / 100.0	30.8 / 72.5 / 97.4",
            0.5: "61.5 / 93.8 / 100.0	21.0 / 52.0 / 79.7",
            0.6: "60.9 / 93.9 / 100.0	17.5 / 40.8 / 61.1",
            0.7: "60.6 / 93.8 / 99.9	13.3 / 35.2 / 54.1",
            0.8: "60.5 / 93.8 / 99.9	11.7 / 35.0 / 52.2",
            0.9: "61.0 / 93.8 / 99.9	11.7 / 33.8 / 49.9",
            1.0: "60.8 / 93.8 / 99.9	11.9 / 33.6 / 49.7",
        },
    },
    "last": {
        "salad": {
            0.1: "44.8 / 80.6 / 98.8	4.7 / 17.2 / 58.3",
            0.2: "60.8 / 92.9 / 100.0	26.8 / 66.9 / 95.3",
            0.3: "60.3 / 93.7 / 100.0	31.2 / 78.1 / 98.6",
            0.4: "61.1 / 93.7 / 100.0	29.1 / 74.6 / 99.1",
            0.5: "61.7 / 93.8 / 100.0	23.3 / 58.7 / 86.2",
            0.6: "60.9 / 93.8 / 100.0	16.8 / 44.3 / 68.5",
            0.7: "61.0 / 93.8 / 100.0	12.8 / 37.8 / 57.6",
            0.8: "61.1 / 93.8 / 99.9	12.1 / 34.3 / 53.1",
            0.9: "61.0 / 93.8 / 99.9	11.2 / 33.8 / 49.7",
            1.0: "60.8 / 93.8 / 99.9	11.9 / 33.6 / 49.7",
        },
    },
    "center": {
        "salad": {
            0.1: "45.3 / 81.0 / 99.0	4.4 / 17.7 / 58.0",
            0.2: "60.7 / 92.9 / 100.0	27.7 / 67.4 / 95.3",
            0.3: "60.6 / 93.3 / 100.0	32.4 / 81.8 / 98.8",
            0.4: "61.2 / 93.6 / 100.0	29.4 / 74.4 / 98.6",
            0.5: "61.3 / 93.9 / 100.0	24.0 / 58.3 / 85.3",
            0.6: "60.7 / 93.7 / 100.0	15.6 / 42.2 / 64.8",
            0.7: "60.8 / 93.8 / 100.0	13.5 / 36.1 / 56.6",
            0.8: "60.8 / 93.8 / 99.9	12.4 / 35.4 / 51.7",
            0.9: "60.9 / 93.8 / 99.9	11.7 / 33.1 / 49.4",
            1.0: "60.8 / 93.8 / 99.9	11.9 / 33.6 / 49.7",
        },
    },
}


def find_numbers(string_, return_numbers=False):
    pattern = r"[-+]?(?:\d*\.*\d+)"
    # res = "53.2 / 85.8 / 95.3	3.5 / 11.7 / 25.2"
    matches = re.findall(pattern, string_)
    numbers = list(map(float, matches))
    if return_numbers:
        return numbers
    avg = sum(numbers) / len(matches)
    return avg


def main():
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.sans-serif": ["Helvetica"],
        "font.size": 12,  # Set the global font size
        "text.latex.preamble": r"\usepackage{amsmath}", })
    plt.figure(figsize=(5, 7))

    plt.subplot(211)
    ds = aachen
    plt.ylim(0, 100)
    plt.xticks(np.arange(1, 11) / 10)
    plt.xlabel(r"$\lambda$")
    plt.ylabel("% successfully localized images")
    markers = {
        "first": "o",
        "center": "d",
        "last": "v",
        "random-0": "h",
        "gaussian": "*",
    }
    tableau_colors = plt.get_cmap('tab10')

    colors = {
        "first": tableau_colors(0),
        "center": tableau_colors(1),
        "last": tableau_colors(2),
        "random-0": tableau_colors(3),
        "gaussian": tableau_colors(4),
    }
    orders_ = ["first", "center", "last", "random-0", "gaussian"]
    plt.title("Aachen Day/Night v1.1")
    plt.axhline(y=92.1, color="r", linestyle="--", label="hloc")
    plt.axhline(y=80.3, color="b", linestyle="--", label="vanilla")

    for order_ in orders_:
        all_numbers = []
        for method_ in ds[order_]:
            for param_ in ds[order_][method_]:
                res = ds[order_][method_][param_]
                avg_res = find_numbers(res)
                all_numbers.append(avg_res)
        # method_ = f"{method_}-{order_}"
        print(order_, max(all_numbers))
        plt.plot(
            np.arange(1, 11) / 10, all_numbers, marker=markers[order_], label=order_,
            color=colors[order_]
        )
    plt.legend(loc=4, fontsize=9, ncol=1)

    plt.subplot(212)

    ds = robotcar
    plt.ylim(0, 100)
    plt.xticks(np.arange(1, 11) / 10)
    plt.xlabel(r"$\lambda$")
    plt.ylabel("% successfully localized images")

    plt.title("RobotCar Seasons v2")
    plt.axhline(y=78.5, color="r", linestyle="--", label="hloc")
    plt.axhline(y=58.3, color="b", linestyle="--", label="vanilla")

    for order_ in orders_:
        all_numbers = []
        for method_ in ds[order_]:
            for param_ in ds[order_][method_]:
                res = ds[order_][method_][param_]
                avg_res = find_numbers(res)
                all_numbers.append(avg_res)
        print(order_, max(all_numbers))
        plt.plot(
            np.arange(1, 11) / 10, all_numbers, marker=markers[order_], label=order_,
            color=colors[order_]

        )
    plt.legend(loc=4, fontsize=9, ncol=1)
    plt.tight_layout()

    plt.savefig(
        "ablation_order.pdf", format="pdf", dpi=600, bbox_inches="tight", pad_inches=0.1
    )


if __name__ == "__main__":
    main()
