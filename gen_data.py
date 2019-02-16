import numpy as np
import pandas as pd
import copy


# version 2


k_over_l_values = np.arange(0, 20000, 25)
# number from lecture 2/13
e = 1000
g = .1  # exaggerated for visual effect (according to a 2015 BLS report, growth is at around 0.011)
n = 0.02
s = 0.2
savings = 0.2
savings_2 = 0.25
depreciation = 0.05
alpha = .2  # please keep alpha at most .9, graph breaks down at values above
y_over_k = (depreciation + g + n) / savings
y_over_k_2 = (depreciation + g + n) / savings_2
time_periods = 5


class Change_Request:
    def __init__(self, time_period, param_to_change, new_val):
        self.time_period = time_period
        self.param_to_change = param_to_change
        self.new_val = new_val
    def __repr__(self):
        return "{} {} {}".format(self.time_period, self.param_to_change, self.new_val)


class Properties:
    def __init__(self, alpha, e, g, n, s, d, delta_g=0,
                 delta_n=0, delta_d=0, delta_s=0):
        self.alpha = alpha
        self.e = e
        self.g = g
        self.n = n
        self.s = s
        self.d = d
        self.delta_g = delta_g
        self.delta_n = delta_n
        self.delta_d = delta_d
        self.delta_s = delta_s

    def grow_one_period(self):
        self.g = self.g * (1 + self.delta_g)
        self.n = self.n * (1 + self.delta_n)
        self.d = self.d * (1 + self.delta_d)
        self.s = self.s * (1 + self.delta_s)
        self.e = self.e * (1 + self.g)

    def copy(self):
        return Properties(self.alpha, self.e, self.g, self.n, self.s, self.d, self.delta_g,
                          self.delta_n, self.delta_d, self.delta_s)


def gen_single_point_data(alpha, e, g, n, s, d, k_over_l):
    y_over_l = k_over_l ** alpha * e ** (1 - alpha)
    return y_over_l


def gen_single_time_data(alpha, e, g, n, s, d, k_over_l_values):
    y_over_l_values = k_over_l_values ** alpha * e ** (1 - alpha)
    y_over_k = (d + g + n) / s
    BGE_y_over_l = (1 / y_over_k) ** (alpha / (1 - alpha)) * e

    return y_over_l_values, BGE_y_over_l, y_over_k


def gen_multiple_time_data(props, k_over_l_values, start_time, end_time, point=None):
    data = {"t": [], "y_over_l": [], "y_over_k": [], "k_over_l": [], "bge": [],
            "metadata": [], "point": []}
    for index, period in enumerate(range(start_time, end_time)):
        y_over_l_vals, BGE_y_over_l, y_over_k = gen_single_time_data(props.alpha, props.e,
                                                                     props.g, props.n, props.s,
                                                                     props.d, k_over_l_values)
        data["t"].append(period)
        data["y_over_l"].append(y_over_l_vals)
        data["bge"].append(BGE_y_over_l)
        data["y_over_k"].append(y_over_k)
        data["k_over_l"].append(k_over_l_values)
        data["metadata"].append(vars(props))
        if point:
            point[0] = gen_single_point_data(props.alpha, props.e,
                                             props.g, props.n, props.s,
                                             props.d, point[1])
            data["point"].append(copy.copy(point))
            savings = props.s * point[0]
            depreciation = (props.n + props.d) * point[1]
            point[1] = point[1] + savings - depreciation

        elif not point:
            data["point"].append(BGE_y_over_l)
        props.grow_one_period()

    return data


def get_k_over_l_range(props, time):
    graph_scaling_factor = 1.1
    y_over_k, max_y_over_l, max_k_over_l = get_bge_y_over_l(props, time)
    top_k_over_l = max_k_over_l * graph_scaling_factor
    step_size = top_k_over_l / 1000
    return top_k_over_l, step_size


def get_bge_y_over_l(props, time):
    y_over_k = (props.g + props.n + props.d) / props.s
    y_over_l = (1 / y_over_k) ** (props.alpha / (1 - props.alpha)) * (props.e * (1 + props.g) ** time)
    k_over_l = y_over_l / y_over_k
    return (y_over_k, y_over_l, k_over_l)


def combine_data(d1, d2):
    for key in list(d1.keys()):
        d1[key].extend(d2[key])
    return d1


def dynamic_change(props, total_time, change_requests=[]):
    curr_time = 0
    change_requests = list(filter(lambda x: x.time_period < total_time,
                             sorted(change_requests, key=lambda x: x.time_period)))
    initial_data = get_bge_y_over_l(props, 0)
    initial_point = [initial_data[1], initial_data[2]]
    print(change_requests)

    # range prediction
    temp_props = props.copy()
    for r in change_requests:
        setattr(temp_props, r.param_to_change, r.new_val)
    top_k_over_l, step_size = get_k_over_l_range(temp_props, total_time * 1.01)

    # actual loop
    consolidated_data = {"t": [], "y_over_l": [], "y_over_k": [],
                         "k_over_l": [], "bge": [], "metadata": [], "point": []}
    for r in change_requests:
        print(r)
        consolidated_data = combine_data(consolidated_data,
                                         gen_multiple_time_data(props, np.arange(0, top_k_over_l, step_size), curr_time,
                                                                r.time_period, point=initial_point))
        curr_time = r.time_period
        setattr(props, r.param_to_change, r.new_val)

    consolidated_data = combine_data(consolidated_data,
                                     gen_multiple_time_data(props, np.arange(0, top_k_over_l, step_size), curr_time,
                                                            total_time, point=initial_point))
    return consolidated_data


def calc_percent_change(df):
    df["point_y_over_l"] = df["point"].apply(lambda x: x[0])
    df["point_k_over_l"] = df["point"].apply(lambda x: x[1])
    df["change_in_y_over_l"] = df["point_y_over_l"].pct_change().apply(lambda x: np.round(x, decimals=5))
    df["change_in_k_over_l"] = df["point_k_over_l"].pct_change().apply(lambda x: np.round(x, decimals=5))
    df["change_in_bge_y_over_l"] = df["bge"].pct_change().apply(lambda x: np.round(x, decimals=5))
    df["bge_k_over_l"] = df["bge"] * df["y_over_k"] ** -1
    df["change_in_bge_k_over_l"] = df["bge_k_over_l"].pct_change().apply(lambda x: np.round(x, decimals=5))
    return df


def produce_data(p, time_limit, changes):
    data = pd.DataFrame(dynamic_change(p, time_limit, changes))
    data = calc_percent_change(data)
    return data, vars(p)


# test_p = Properties(alpha, e, 0.02, n, s, depreciation)
# original_test_p = test_p.copy()
# test_changes = [Change_Request(5, "s", 0.50), Change_Request(70, "n", 0.07)]
# produce_data(original_test_p, 100, test_changes)