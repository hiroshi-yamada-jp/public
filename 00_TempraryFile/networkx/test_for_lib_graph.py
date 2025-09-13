"""
概要: Networkxの初期設定用ライブラリの動作確認
状態: OK 2025/09/06
備考: chatgpt-AIで自動生成
"""
import sys
from pprint import pprint
# 拡張ライブラリ
import networkx as nx
# テスト対象ライブラリ
from lib_networkx.lib_graph import (
    create_multigraph, get_graph_attrs, update_graph_attrs, draw_multigraph,
    add_node, add_nodes_bulk, query_nodes, query_nodes_by_key, get_node, update_node_attrs,
    add_edge, add_edges_bulk, query_edges, query_edges_by_attr, get_edge, update_edge_attrs,
    get_simple_path, verify_path, get_shortest_path, get_adjacent_nodes, get_connected_edges
)

# ==========================
#  ノード & エッジパラメータ
# ==========================
params_nodes = [
    {"id": i, "name": f"Node{i}", "type": F"t{i % 3}"} for i in range(1, 14)
]

NO = 0
params_edges = [
    {"node1_id": 1, "route1_id": 1, "node2_id": 2, "route2_id": 1, "edge_id": NO + 1},
    {"node1_id": 2, "route1_id": 2, "node2_id": 3, "route2_id": 1, "edge_id": NO + 2},
    {"node1_id": 3, "route1_id": 2, "node2_id": 4, "route2_id": 2, "edge_id": NO + 3},
    {"node1_id": 4, "route1_id": 2, "node2_id": 5, "route2_id": 1, "edge_id": NO + 4},
    {"node1_id": 5, "route1_id": 2, "node2_id": 6, "route2_id": 1, "edge_id": NO + 5},
    {"node1_id": 6, "route1_id": 2, "node2_id": 7, "route2_id": 1, "edge_id": NO + 6},
    {"node1_id": 7, "route1_id": 2, "node2_id": 8, "route2_id": 1, "edge_id": NO + 7},
    {"node1_id": 8, "route1_id": 2, "node2_id": 9, "route2_id": 1, "edge_id": NO + 8},
    {"node1_id": 10, "route1_id": 1, "node2_id": 11, "route2_id": 2, "edge_id": NO + 9},
    {"node1_id": 11, "route1_id": 2, "node2_id": 12, "route2_id": 1, "edge_id": NO + 10},
    {"node1_id": 12, "route1_id": 2, "node2_id": 11, "route2_id": 3, "edge_id": NO + 11},
    {"node1_id": 1, "route1_id": 2, "node2_id": 4, "route2_id": 3, "edge_id": NO + 12},
    {"node1_id": 1, "route1_id": 3, "node2_id": 6, "route2_id": 3, "edge_id": NO + 13},
    {"node1_id": 6, "route1_id": 4, "node2_id": 9, "route2_id": 2, "edge_id": NO + 14},
    {"node1_id": 11, "route1_id": 4, "node2_id": 12, "route2_id": 3, "edge_id": NO + 15},

]

# ==========================
# テスト実行
# ==========================
print("\n== グラフ関係")
# グラフ作成
params_graph = {
    "name": "TestGraph",  # 必須属性
    "graph_id": 101,  # 必須属性
    "device_type": "Router",  # 任意属性
    "任意属性": [1, 2, 3],  # 任意属性
}
G = create_multigraph(**params_graph)
print(f"= グラフ作成: create_multigraph(params_graph)={type(G)}")
print(f"\t{G.graph}")
print(f"\tパラメータ:{params_graph=}")

# グラフ属性取得
res = get_graph_attrs(G)
print(f"= グラフ属性取得: get_graph_attrs(G)={type(res)}\n\t{res}")

# グラフ属性更新
params_update_graph = {"location": "Tokyo", "version": "1.0"}
update_graph_attrs(G, params_update_graph)
res = get_graph_attrs(G)
print(f"= グラフ属性更新: update_graph_attrs(G, params_update_graph)={type(res)}\n\t{res}")
print(f"\tパラメータ:{params_update_graph=}")

print("\n== ノード関係")
# ノード一括登録
params = params_nodes
res = add_nodes_bulk(G, params)
print(f"= ノード一括登録: add_nodes_bulk(G, params)={type(res)}\t{len(res)}")
pprint(res, indent=4)
print(F"パラメータ:{len(params)=}")
pprint(params, indent=4)

# 指定ノード検索
for node_id in range(2, 10):
    res = get_node(G, node_id=node_id)
    print(f"\n\t指定IDのノード: get_node(G, {node_id=})={res}")
    # 指定ノードの属性更新
    params_update_node = {"key": F"key{node_id % 3}", "type": F"new_t{node_id % 3}"}
    params = (node_id, params_update_node)
    res = update_node_attrs(G, *params)
    print(f"\t指定ノード更新: update_node_attrs(G, *params)={res}")
    print(f"\t{params=}")

# ノード一覧の取得
res = query_nodes(G)
print(f"= ノード一覧: query_nodes(G)={type(res)}\t{len(res)}")
pprint(res, indent=4)

# 指定条件のノード一覧の取得
params = {"type": "new_t2", "key": "key2"}
res = query_nodes_by_key(G, conditions=params)
print(f"= 指定条件のノード一覧: query_nodes_by_key(G,conditions={params})={type(res)}\t{len(res)}")
pprint(res, indent=4)

print("\n== エッジ関係")
# エッジ一括登録
params = params_edges
res = add_edges_bulk(G, params)
print(f"= エッジ一括登録: add_edges_bulk(G, params)={type(res)}\t{len(res)}")
pprint(res, indent=4, width=120)
print(f"\t{params=}")

for i, param in enumerate(params_edges):
    # 指定エッジ取得
    if i == 6:
        break
    n1, n2, r1, r2 = param["node1_id"], param["node2_id"], param["route1_id"], param["route2_id"],
    res = get_edge(G, n1, n2, route1_id=r1, route2_id=r2)
    print(f"= 指定エッジ取得: get_edge(G, {n1}, {n2}, route1_id={r1}, route2_id={r2})={type(res)}\n\t{res}")
    params_update_edge = {"latency": "10ms", "type": F"t{i % 3}"}
    # エッジ属性更新
    res = update_edge_attrs(G, n1, n2, route1_id=r1, route2_id=r2, new_attrs=params_update_edge)
    func = f"update_edge_attrs(G, node1_id=1, route1_id=1, node2_id=2, route2_id=1,{params_update_edge})"
    print(f"= エッジ属性更新: {func}={type(res)}\n\t{res}")

# エッジ一覧取得
res = query_edges(G)
print(f"= エッジ一覧: query_edges(G)={type(res)}\t{len(res)}")
pprint(res, indent=4, width=160)

# 指定条件に合致するエッジ一覧取得
res = query_edges_by_attr(G, key="edge_id", value=1)
print(f"= エッジ検索:query_edges_by_attr(G, key='edge_id', value=1)={type(res)}\t{len(res)}")
pprint(res, indent=4, width=160)

res = query_edges_by_attr(G, key="route1_id", value=2)
print(f"= エッジ検索:query_edges_by_attr(G, key='route1_id', value=2)={type(res)}\t{len(res)}")
pprint(res, indent=4, width=160)

print("\n== パス関係")
# 最短パス取得
test_params = [(1, 6), (2, 9), (3, 8), (8, 11), (11, 12)]
print(f"\n= 開始終了パスの最短パス・全パス取得")
for node1_id, node2_id in test_params:
    res = get_shortest_path(G, node1_id=node1_id, node2_id=node2_id)
    print(f"\t最短パス: get_shortest_path(G, {node1_id=},{node2_id=})={res}\t{type(res)}")
    res = get_simple_path(G, node1_id=node1_id, node2_id=node2_id)
    print(f"\t全パス: get_simple_path(G, {node1_id=},{node2_id=})=={res}\t{type(res)}")

# 指定パス検証
test_params = [
    [1, 2, 3, 4, 5],
    [2, 1, 5],
    [11, 12],
    [11, 12, 2],
    [10, 11],
    [2, 1, 5, 7],
]
print(f"\n= 指定パスの接続検証")
for params in test_params:
    res = verify_path(G, path=params)
    print(f"\tverify_path(G, path={params})={res}\t{type(res)}")

# 隣接ノード & 接続エッジ一覧
print(f"\n= 隣接ノード & 接続エッジ一覧")
for node_id in [1, 3, 5, 11, 12, 13]:
    res = get_adjacent_nodes(G, node_id=node_id)
    print(f"\n隣接ノード: get_adjacent_nodes(G, {node_id=})={type(res)}\t{len(res)=}")
    pprint(res, indent=4, width=120)

    res = get_connected_edges(G, node_id=node_id)
    print(f"接続エッジ: get_connected_edges(G, {node_id=})={type(res)}\t{len(res)=}")
    pprint(res, indent=4, width=120)

# グラフ描画（最後に追加）
show_enable = True
# show_enable = False
pos = nx.spring_layout(G, seed=42)
if show_enable:
    draw_multigraph(G)
