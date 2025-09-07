"""
概要: Networkxの初期設定用ライブラリの動作確認
状態: OK 2025/09/06
備考: chatgpt-AIで自動生成
"""
# 拡張ライブラリ
import networkx as nx
# テスト対象ライブラリ
from lib_networkx.lib_graph import (
    create_multigraph, get_graph_attrs, update_graph_attrs, draw_multigraph,
    add_node, add_nodes_bulk, get_nodes, find_target_node, update_node_attrs,
    add_edge, add_edges_bulk, get_edges, find_target_edge, update_edge_attrs,
    get_simple_path, verify_path, get_adjacent_nodes, get_shortest_path
)

# ==========================
# テスト用パラメータ定義
# ==========================
params_nodes = [
    {"id": i, "name": f"Node{i}", "description": f"Node {i} 新規登録"} for i in range(1, 13)
]

edges1 = [{"node1_id": i, "route1_id": 1, "node2_id": i + 1, "route2_id": 1} for i in range(1, 9)]
edges2 = [
    {"node1_id": 1, "route1_id": 2, "node2_id": 2, "route2_id": 2},
    {"node1_id": 3, "route1_id": 2, "node2_id": 4, "route2_id": 2},
    {"node1_id": 1, "route1_id": 3, "node2_id": 5, "route2_id": 2},
    {"node1_id": 1, "route1_id": 4, "node2_id": 9, "route2_id": 2},
    {"node1_id": 11, "route1_id": 1, "node2_id": 12, "route2_id": 1},
    {"node1_id": 12, "route1_id": 2, "node2_id": 11, "route2_id": 2},

]
params_edges = edges1 + edges2

# ==========================
# テスト実行
# ==========================
params_graph = {
    "name": "TestGraph",
    "graph_id": 101,
    "device_type": "Router"
}

print("\n== グラフ関係")
# グラフ作成
G = create_multigraph(**params_graph)
print(f"= グラフ作成: create_multigraph({params_graph})={type(G)}")
print(f"グラフの内容: {G.graph=}")

# グラフ属性取得
res = get_graph_attrs(G)
print(f"= グラフ属性取得: get_graph_attrs(G)={res}\t{type(res)}")

# グラフ属性更新
params_update_graph = {"location": "Tokyo", "version": "1.0"}

params = params_update_graph
update_graph_attrs(G, params)
res = get_graph_attrs(G)
print(f"= グラフ属性更新: update_graph_attrs(G, {params})={res}\t{type(res)}")

print("\n== ノード関係")
# ノード一括登録
params = params_nodes
res = add_nodes_bulk(G, params)
print(f"= ノード一括登録: add_nodes_bulk(G, params)={type(res)}\t{len(res)}\n\t{res}")
print(f"\t{params=}")

# ノード一覧取得（詳細）
res = get_nodes(G, minimal=False)
print(f"= ノード一覧取得（詳細）: get_nodes(G, minimal=False)={type(res)}\t{len(res)}\n\t{res}")

# ノード一覧取得（簡易）
res = get_nodes(G, minimal=True)
print(f"= ノード一覧取得（簡易）: get_nodes(G, minimal=True)={type(res)}\t{len(res)}\n\t{res}")

# ノード検索
res = find_target_node(G, node_id=5)
print(f"= ノードをIDで検索: find_target_node(G, node_id=5)={res}\t{type(res)}")

# ノード属性更新
params_update_node = {"description": "Updated node", "memo": "新属性を追加"}
params = (5, params_update_node)
res = update_node_attrs(G, *params)
print(f"= ノード属性更新: update_node_attrs(G, params)={res}\t{type(res)}")
print(f"\t{params=}")

print("\n== エッジ関係")

# エッジ一括登録
params = params_edges
res = add_edges_bulk(G, params)
print(f"= エッジ一括登録: add_edges_bulk(G, params)={type(res)}\t{len(res)}\n\t{res}")
print(f"\t{params=}")

# エッジ一覧取得（詳細）
res = get_edges(G, minimal=False)
print(f"= エッジ一覧取得（詳細）: get_edges(G, minimal=False)={type(res)}\t{len(res)}\n\t{res}")
res = get_edges(G, minimal=True)
print(f"= エッジ一覧取得（簡易）: get_edges(G, minimal=True)={type(res)}\t{len(res)}\n\t{res}")

# エッジ検索
res = find_target_edge(G, node1_id=1, route1_id=1, node2_id=2, route2_id=1)
print(f"= エッジ検索: find_target_edge(G, node1_id=1, route1_id=1, node2_id=2, route2_id=1)={type(res)}\n\t{res}")

# エッジ属性更新
params_update_edge = {"bandwidth": "1Gbps", "latency": "10ms"}

res = update_edge_attrs(G, node1_id=1, route1_id=1, node2_id=2, route2_id=1, new_attrs=params_update_edge)
func = f"update_edge_attrs(G, node1_id=1, route1_id=1, node2_id=2, route2_id=1,{params_update_edge})"
print(f"= エッジ属性更新: {func}={type(res)}\n\t{res}")

print("\n== パス関係")
# 最短パス取得
test_params = [(1, 6), (2, 9), (3, 8), (8, 11), (11, 12)]
print(f"\n= 最短パス取得: get_shortest_path")
for node1_id, node2_id in test_params:
    res = get_shortest_path(G, node1_id, node2_id)
    print(f"get_shortest_path(G, {node1_id},{node2_id})={res}\t{type(res)}")

    res = get_simple_path(G, node1_id, node2_id)
    print(f"get_simple_path(G, {node1_id},{node2_id})={res}\t{type(res)}")

# 指定ノード間のパス数カウント
print(f"\n= 指定ノード間のパス数カウント")
for start_id, end_id in test_params:
    params = (start_id, end_id)
    params = (start_id, end_id)

# 指定パス検証
test_params = [
    [1, 2, 3, 4, 5],
    [2, 1, 5],
    [11, 12],
    [11, 12, 2],
    [10, 11],
    [2, 1, 5, 7],

]
print(f"\n= 指定パス検証")
for params in test_params:
    res = verify_path(G, params)
    print(f"verify_path(G, {params})={res}\t{type(res)}")

# 隣接ノード取得
print(f"\n= 隣接ノード取得")
for params in [1, 3, 5, 10, 11, 12]:
    res = get_adjacent_nodes(G, params)
    print(f"get_adjacent_nodes(G, {params})=={type(res)}\t{len(res)=}\n\t{res}")

# グラフ描画（最後に追加）
show_enable = True
pos = nx.spring_layout(G, seed=42)
if show_enable:
    draw_multigraph(G)
