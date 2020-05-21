import copy
import numpy as np


def _dfs(v: int, adjacency_matrix: list, used: list, matching: list):  # v - node
    if used[v]:
        return False
    used[v] = True
    for u, link_exists in enumerate(adjacency_matrix[v]):
        if link_exists != 0:
            if (matching[u] == -1 or _dfs(matching[u], adjacency_matrix, used, matching)):
                matching[u] = v
                return True
    return False


def khun_method(adjacency_matrix: list):
    nodes_amount = len(adjacency_matrix)
    matching = list()
    for i in range(0, nodes_amount):
        matching.append(-1)
    for i in range(0, nodes_amount):
        used = [False] * nodes_amount
        _dfs(i, adjacency_matrix, used, matching)
    result = []
    for i in range(0, nodes_amount):
        if matching[i] != -1:
            result.append((matching[i], i))
    return result  # return pairs


def _find_min_and_subtract(price_matrix: list):
    for row_idx, row in enumerate(price_matrix):
        min_in_row = min(row)
        row = [row_item - min_in_row for row_item in row]
        price_matrix[row_idx] = row
    price_matrix_transposed = np.array(price_matrix).transpose()
    for row_idx, row in enumerate(price_matrix_transposed):
        min_in_row = min(row)
        row = [row_item - min_in_row for row_item in row]
        price_matrix_transposed[row_idx] = row

    new_price_matrix = price_matrix_transposed.transpose().tolist()
    return new_price_matrix


def _get_adjacency_from_price_matrix(price_matrix: list):
    adjacency_matrix = []
    for row in price_matrix:
        adjacency_matrix_row = []
        for row_item in row:
            if row_item == 0:
                adjacency_matrix_row.append(1)
            else:
                adjacency_matrix_row.append(0)
        adjacency_matrix.append(adjacency_matrix_row)
    return adjacency_matrix


def _get_zero_coverage(price_matrix: list, connection_pairs: list):
    nodes_amount = len(price_matrix)
    covered_rows, covered_cols = {row for row in range(0, nodes_amount)}, set()
    # step 1: all rows without marked zeros
    for pair in connection_pairs:
        covered_rows.remove(pair[0])  # remove marked rows

    while True:
        new_items_were_added = False
        for covered_row in covered_rows:
            for item_col_idx, covered_row_item in enumerate(price_matrix[covered_row]):
                if covered_row_item == 0 and item_col_idx not in covered_cols:
                    covered_cols.add(item_col_idx)
                    new_items_were_added = True

        if new_items_were_added == False:
            return {row for row in range(0, nodes_amount)} - covered_rows, covered_cols
        else:
            new_items_were_added = False

        for covered_col in covered_cols:
            for price_matrix_row_idx, price_matrix_row in enumerate(price_matrix):
                if price_matrix_row[covered_col] == 0 and (
                        price_matrix_row_idx,
                        covered_col) in connection_pairs and price_matrix_row_idx not in covered_rows:
                    covered_rows.add(price_matrix_row_idx)
                    new_items_were_added = True

        if new_items_were_added == False:
            return {row for row in range(0, nodes_amount)} - covered_rows, covered_cols


def _proc_price_matrix(price_matrix, covered_rows, covered_cols):
    not_covered_elemnts = []
    for row_idx, price_matrix_row in enumerate(price_matrix):
        for col_idx, row_item in enumerate(price_matrix_row):
            if row_idx not in covered_rows and col_idx not in covered_cols:
                not_covered_elemnts.append(row_item)
    min_not_covered_elemnt = min(not_covered_elemnts)
    for row_idx, price_matrix_row in enumerate(price_matrix):
        for col_idx, row_item in enumerate(price_matrix_row):
            if row_idx not in covered_rows and col_idx not in covered_cols:
                price_matrix[row_idx][col_idx] = row_item - min_not_covered_elemnt
            elif row_idx in covered_rows and col_idx in covered_cols:
                price_matrix[row_idx][col_idx] = row_item + min_not_covered_elemnt


def _get_sum_price(price_matrix, connection_pairs):
    sum_price = 0
    for connection_pair in connection_pairs:
        sum_price += price_matrix[connection_pair[0]][connection_pair[1]]
    return sum_price


def hungarian_method(price_matrix: list):
    price_matrix_copy = copy.deepcopy(price_matrix)
    while True:
        price_matrix_copy = _find_min_and_subtract(price_matrix_copy)
        connection_pairs = khun_method(adjacency_matrix=_get_adjacency_from_price_matrix(price_matrix_copy))
        if len(connection_pairs) == len(price_matrix_copy):
            sum = _get_sum_price(price_matrix, connection_pairs)
            return {"Appointments": connection_pairs, "Result sum for work": sum}
        covered_rows, covered_cols = _get_zero_coverage(price_matrix_copy, connection_pairs)
        _proc_price_matrix(price_matrix_copy, covered_rows, covered_cols)


if __name__ == "__main__":
    price_matrix = [[1, 7, 1, 3],
                    [1, 6, 4, 6],
                    [17, 1, 5, 1],
                    [1, 6, 10, 4]]
    print(hungarian_method(price_matrix))
