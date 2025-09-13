"""
概要: Networkxの設定用ライブラリ
状態: OK 2025/09/13
備考: chatgpt-AIで自動生成したものを更新

## AI指示書
networkxを使って以下の関数ライブラリを作成して

### 制約条件
- google styleのdocStringをつける
- 難解なコード部分は何をしているのか解説を加える
- python3.10以降で動作可能な標準型(list/dict/tuple/set)をtype hintに使う
- 作成したライブラリの各関数を動作確認できるテストコードを別ファイルで作成する
テストコードで使用するパラメータは、別変数で定義して、容易に変更できるようにしてください
テストコードには、最低10個以上のノードとエッジを含んでください
テストコードの結果は、各関数の実行結果の戻り値がわかるように以下の形式で表示してください
params = [1,2,3]
res = func1(params)
print(F"\n= 機能説明: func1({params})= {type(res)} \n{res}"


### 作成する関数一覧
== グラフ操作関数
- 無向マルチグラフの新規作成（追加する属性パラメータ：名前、ID、デバイスタイプ)
- 作成したマルチグラフの属性一覧を取得(パラメータ: ID)
- 作成したマルチグラフに属性を追加、更新

== ノード操作関数
- グラフにノード登録(パラメータ：name,id,status,description)
- 上記のノード登録関数を使って複数ノード一覧を一括登録し、登録結果を返す(パラメータ: 辞書型のノードリスト。リスト内の各要素に名前とIDは必ず含み、その他は省略可能)
- 作成したノード一覧リストを取得し、全属性を含んだ一覧を返す。(パラメータ: 名前とIDのみを返すオプションパラメータ)
- グラフ内の登録ノードをノードIDで検索し、全属性を含んだノードを返す(パラメータ: node_id)
- 作成したノードに属性を追加、更新
- 指定ノードに隣接するノード一覧を抽出
- 二つの任意ノードの最短パスを返す。パスが見つからない場合はNoneを返す

== エッジ操作関数
- グラフにエッジ登録（パラメータ、エッジ一覧(node1_id,node1_route_id,node2_id,node2_route_id)
- 上記のエッジ登録関数を使って複数エッジを一括登録(パラメータ: 辞書型のエッジ一覧リスト。名前とIDはリストは必ず含み、その他は省略可能)
- 作成したエッジ一覧リスト取得(全属性を含んだ一覧を返す。オプションパラメータ指定で名前とIDのみを返すことも可能にする)
- 作成したエッジに属性を追加、更新
- グラフ内の登録エッジをエッジIDで検索し取得する(全属性を含んだエッジを返す)

== パス検索関数
- 二つの任意ノード間の最短パスを返す。見つからない場合はNoneを返す
- 二つの任意ノード間にパスが存在するか判定、見つかった経路数を返す。見つからない場合は経路数に0を返す
- 二つの任意ノード間の指定パスが存在するか確認し、確認結果を返す(パラメータ：開始ノード、任意の数の中間ノード、終了ノード)

networkxの関数仕様の概要
1. ノード間の「リンク（エッジ）」取得関数
G.has_edge(u, v): ノード間にエッジが存在するか判定 :u, v: 始点・終点ノードID
G.get_edge_data(u, v): ノード間のエッジ属性を取得（MultiGraphでは辞書）: u, v: 始点・終点ノードID, key（任意）:ユニークキー
G.edges(u, v, data=True) ノード間のすべてのエッジを列挙 data=True で属性付き
G[u][v]:  隣接辞書からエッジ情報を取得（MultiGraphではキー付き辞書）: u, v: 始点・終点ノードID

2. ノード間の「パス（経路）」を取得する関数 source, target:始点・終点ノードを示す
nx.shortest_path(G, source, target): 最短経路を返す  
nx.all_shortest_paths(G, source, target): 最短経路が複数ある場合、すべて返す
nx.all_simple_paths(G, source, target): 単純パス（ノード重複なし）をすべて列挙   cutoff: 最大長の指定
nx.has_path(G, source, target) : パスが存在するか判定
nx.single_source_shortest_path(G, source): sourceから全ノードへの最短経路
| nx.edge_dfs(G, source) | エッジベースでグラフを深さ優先探索する関数。MultiGraphで有効
| nx.edge_bfs(G, source) | エッジベースでグラフを幅優先探索する関数。MultiGraphで有効

補足
- MultiGraph の場合、G.get_edge_data(u, v) は {key: attr_dict} の形式で返るため、エッジキーを明示的に扱う必要があります。
- パス探索関数は基本的に ノード列を返すため、エッジ属性やキーを含めたパスを得たい場合は、ノード列からエッジ列を再構築する必要があります。
- weight パラメータは、エッジ属性名（例："cost" や "distance"）を指定することで、重み付きグラフとして扱えます。

"""
# 標準関数
from __future__ import annotations
from typing import Any
# 拡張関数
import matplotlib.pyplot as plt
import networkx as nx


# ==========================
# グラフ描画
# ==========================
# noinspection PyPep8Naming,PyArgumentList,PyUnresolvedReferences
def draw_multigraph(G: nx.MultiGraph, with_labels: bool = True, show_edge_keys: bool = True) -> None:
    """MultiGraph を描画し、エッジ key をラベルとして表示する。

    Args:
        G (nx.MultiGraph): 対象グラフ
        with_labels (bool): ノードラベルを表示するか
        show_edge_keys (bool): エッジ key をラベルとして表示するか

    Note:
        - ノードラベルには 'name' 属性があればそれを使用
        - エッジラベルには key を使用（必要に応じて属性も表示可能）
    """
    pos = nx.spring_layout(G, seed=42)
    font_size = 9

    # ノードラベル
    node_labels = {
        node: G.nodes[node].get("name", str(node))
        for node in G.nodes
    }

    # 描画
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", edgecolors="black", node_size=1200)
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7)
    if with_labels:
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=font_size)

    # エッジ key ラベル
    if show_edge_keys:
        edge_labels = {(u, v, k): str(k) for u, v, k in G.edges(keys=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="blue", font_size=font_size)

    plt.title(f"Graph: {G.graph.get('name', 'Unnamed')}", fontsize=12)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


# ==========================
# グラフ操作関数
# ==========================
# noinspection PyPep8Naming,PyUnresolvedReferences
def create_multigraph(graph_id: int, name: str, **kwargs) -> nx.MultiGraph:
    """無向マルチグラフの作成

    Args:
        graph_id (int): グラフ識別ID
        name (str): グラフ名
        **kwargs: 任意キー
    Returns:
        nx.MultiGraph: 属性付きの新規グラフ
    """
    G = nx.MultiGraph()
    G.graph["id"] = graph_id
    G.graph["name"] = name
    # その他の任意属性の追加
    for key, val in kwargs.items():
        G.graph[key] = val
    return G


# noinspection PyPep8Naming,PyUnresolvedReferences
def get_graph_attrs(G: nx.MultiGraph) -> dict:
    """グラフの属性一覧を取得

    Args:
        G (nx.MultiGraph): 対象グラフオブジェクト
    Returns:
        dict: グラフ属性の辞書
    """
    return dict(G.graph)


# noinspection PyPep8Naming,PyUnresolvedReferences
def update_graph_attrs(G: nx.MultiGraph, new_attrs: dict[str, Any]) -> dict:
    """グラフ属性を追加または更新する

    Args:
        G (nx.MultiGraph): 対象グラフ
        new_attrs (dict): 更新または、追加する属性辞書
    Returns:
        dict: 更新後のグラフ属性の辞書
    """
    G.graph.update(new_attrs)
    return dict(G.graph)


# ==========================
# ノード操作関数
# ==========================
# noinspection PyPep8Naming
def query_nodes(G: nx.MultiGraph) -> list[dict]:
    """グラフに登録されているノード一覧の取得

    Args:
        G (nx.MultiGraph): 対象グラフ
    Returns:
        list[dict]: ノード属性の一覧
    """
    return [{"id": n, **attr} for n, attr in G.nodes(data=True)]


# noinspection PyPep8Naming
def query_nodes_by_key(G: nx.MultiGraph, conditions: dict[str, Any]) -> list[dict]:
    """指定属性の全てが指定値と一致するノード一覧を抽出

    Args:
        G (nx.MultiGraph): 対象グラフ
        conditions (dict[str, Any]): 検索条件（キーと値の辞書）
    Returns:
        list[dict]: 条件に一致するノードの情報（{"id": ノードID, ...属性...}）
    """
    return [{"id": n, **attr} for n, attr in G.nodes(data=True)
            if all(attr.get(k) == v for k, v in conditions.items())]


# noinspection PyPep8Naming
def get_node(G: nx.MultiGraph, node_id: int) -> dict | None:
    """指定IDをもつノードを取得

    Args:
        G (nx.MultiGraph): 対象グラフ
        node_id: 対象ノードID
    Returns:
        dict: ノード属性辞書 / None:指定ノードが未登録
    """
    if not G.has_node(node_id):
        return None
    # **G.nodes[node_id]で指定ノードの属性一覧を取得可能
    res = {"id": node_id, **G.nodes[node_id]}
    return res


# noinspection PyPep8Naming
def add_node(G: nx.MultiGraph, node_id: int, name: str, **kwargs) -> dict | None:
    """単一ノードの登録

    Args:
        G (nx.MultiGraph): 対象グラフ
        node_id: ノードID
        name: ノード名(追加属性)
        kwargs: 任意の属性
    Returns:
        dict: 登録内容 / None: None: 登録失敗（追加対象が登録済)
    """
    if G.has_node(node_id):
        # print(F"ERROR: 指定IDのノードは登録済:{node_id=}")
        return None
    G.add_node(node_id, name=name, **kwargs)
    return get_node(G, node_id=node_id)


# noinspection PyPep8Naming
def add_nodes_bulk(G: nx.MultiGraph, node_list: list[dict]) -> list[dict] | None:
    """複数ノードの一括登録

    Args:
        G (nx.MultiGraph): 対象グラフ
        node_list: 登録するノード属性辞書のリスト
    Returns:
         list[dict]: 登録ノード一覧情報 / None: 登録失敗（追加対象のどれかが登録済)
    """
    # 登録済データがないか、全パラメータを検査
    for node in node_list:
        node_id = node["id"]
        if get_node(G, node_id=node_id) is not None:
            # print(F"ERROR: 指定IDのノードは登録済:{node_id=}")
            return None
    # ノードの一括登録
    for node in node_list:
        node_id = node.get("id")
        node_name = node.get("name")
        keys_to_exclude = ["id", "name"]
        # パラメータから除外パラメータを除いた辞書を作成
        kwargs = {k: v for k, v in node.items() if k not in keys_to_exclude}
        add_node(G, name=node_name, node_id=node_id, **kwargs)
    return query_nodes(G)


# noinspection PyPep8Naming
def update_node_attrs(G: nx.MultiGraph, node_id: int, new_attrs: dict) -> dict | None:
    """ノードの属性を更新し、更新後の情報を返す。

    Args:
        G (nx.MultiGraph): 対象グラフ
        node_id: 対象ノードID
        new_attrs (dict): 更新する属性辞書
    Returns:
        dict: 更新後のノード属性情報（ID含む）/ None:更新失敗
    Note:
        - 更新後の属性は ID を含めた辞書として返す
    """
    if not G.has_node(node_id):
        # print(F"ERROR: 指定IDのノードは未登録:{node_id=}")
        return None
    G.nodes[node_id].update(new_attrs)
    res = {"id": node_id, **G.nodes[node_id]}
    return res


# noinspection PyPep8Naming
def get_connected_edges(G: nx.MultiGraph, node_id: int) -> list[tuple]:
    """指定ノードの接続エッジ一覧（接続先ノードIDとkey）を取得

    Args:
        G (nx.MultiGraph): 対象グラフ
        node_id: 対象ノードID
    Returns:
        list[tuple]:接続エッジ一覧（接続先ノードIDとkey） / 空リスト:接続エッジ一が存在しない
    """
    res = []
    if not G.has_node(node_id):
        return []
    # 指定ノードに隣接するノードIDのイテレータから隣接ノードIDを取得
    for neighbor_node_id in G.neighbors(node_id):
        # 隣接ノードとの間にある全エッジ情報の辞書を取得
        for key in G[node_id][neighbor_node_id]:
            data = {"neighbor_node_id": neighbor_node_id, "edge_key": key}
            res.append(data)
    return res


# noinspection PyPep8Naming
def get_adjacent_nodes(G: nx.MultiGraph, node_id: int) -> list[dict]:
    """指定ノードの隣接ノード一覧を取得

    Args:
        G (nx.MultiGraph): 対象グラフ
        node_id: 対象ノードID
    Returns:
        list[dict]: 隣接ノードのIDと属性一覧 / 空リスト:指定ノードまたは隣接ノードが存在しない場合
    """
    if not node_id in G.nodes:
        # print(F"ERROR: 指定IDのノードは未登録:{node_id=}")
        return []
    res = [{"id": neighbor_id, **G.nodes[neighbor_id]} for neighbor_id in G.adj[node_id]]
    return res


# ==========================
# エッジ操作関数
# ==========================
def _generate_edge_key(node1_id: int, node2_id: int, route1_id: int, route2_id: int) -> str:
    """エッジ生成情報からエッジキーを生成する"""
    edge_key = f"{node1_id}:{route1_id}--{node2_id}:{route2_id}"
    return edge_key


# noinspection PyPep8Naming,PyArgumentList
def query_edges(G: nx.MultiGraph) -> list[dict]:
    """エッジ一覧の取得

    Args:
        G (nx.MultiGraph): 対象グラフ
    Returns:
        list[dict]: エッジ属性の一覧
    """
    result = []
    # G.edges(keys=True, data=True): keys=Trueでkey取得が可能となり、data=Trueで属性(attrs)取得が可能となる
    for u, v, k, attrs in G.edges(keys=True, data=True):
        # u:始点ノードid / v:終点ノードID / k: エッジキー / attrs:エッジに付与された属性を示す
        edge_info = {"node1_id": u, "node2_id": v, "key": k}
        result.append({**edge_info, **attrs})
    return result


# noinspection PyPep8Naming,PyArgumentList
def query_edges_by_attr(G: nx.MultiGraph, key: str, value: Any) -> list[dict]:
    """指定属性キーと値に一致するエッジ一覧を構造化して取得

    Args:
        G (nx.MultiGraph): 対象グラフ
        key (str): 検索対象の属性キー
        value (Any): 一致させたい属性値
    Returns:
        list[dict]: 条件に一致するエッジ情報（source, target, key, 属性含む）
    """
    res = [{"node1_id": u, "node2_id": v, "key": k, **attr} for u, v, k, attr in G.edges(keys=True, data=True)
           if attr.get(key) == value]
    return res


# noinspection PyPep8Naming,PyTypeChecker
def get_edge(G: nx.MultiGraph, node1_id: int, node2_id: int, *, route1_id: int, route2_id: int) -> dict | None:
    """指定情報に合致するエッジを取得

    Args:
        G (nx.MultiGraph): 対象グラフ
        node1_id: 始点ノードID
        node2_id: 終点ノードID
        route1_id: 始点ルートID
        route2_id: 終点ルートID
    Returns:
        dict: エッジ属性辞書 / None:指定エッジが未登録
    Note:
        networkx の MultiGraph は同じノード間に複数エッジを持つため、各エッジは一意なキーで識別される
    """
    key = _generate_edge_key(node1_id, node2_id, route1_id=route1_id, route2_id=route2_id)
    if not G.has_edge(u=node1_id, v=node2_id, key=key):
        return None
    # u(node1_id),v(node2_id),k(key) が一致するエッジの属性辞書を抽出 例: {'route1_id': 1, 'route2_id': 1}
    attr = G.edges[node1_id, node2_id, key]
    return {
        "node1_id": node1_id,
        "node2_id": node2_id,
        "key": key,
        **attr
    }


# noinspection PyPep8Naming
def add_edge(G: nx.MultiGraph, node1_id: int, node2_id: int, *, route1_id: int, route2_id: int,
             edge_id: int) -> dict | None:
    """エッジを登録する（route ID に基づく固有キー付き）

    Args:
        G (nx.MultiGraph): 対象グラフ
        node1_id: 始点ノードID
        node2_id: 終点ノードID
        route1_id: 始点ルートID
        route2_id: 終点ルートID
        edge_id: エッジID
    Returns:
        dict: 登録内容 /None: 登録失敗（同一エッジ登録済)
    Note:
        同一ノード間のエッジでも route1 & route2 ID が異なれば別エッジとして扱う
    """
    # 恩地エッジが登録済の場合、登録失敗
    if get_edge(G, node1_id, node2_id, route1_id=route1_id, route2_id=route2_id) is not None:
        # print(F"ERROR: 指定エッジは登録済:{node1_id=}\t{node2_id=}")
        return None
    attr = {"route1_id": route1_id, "route2_id": route2_id, "edge_id": edge_id}
    key = _generate_edge_key(node1_id, node2_id, route1_id=route1_id, route2_id=route2_id)
    G.add_edge(node1_id, node2_id, key=key, **attr)
    # 登録内容を返す
    return get_edge(G, node1_id, node2_id, route1_id=route1_id, route2_id=route2_id)


# noinspection PyPep8Naming
def add_edges_bulk(G: nx.MultiGraph, edge_list: list[dict]) -> list[dict]:
    """複数エッジを一括登録する

    Args:
        G (nx.MultiGraph): 対象グラフ
        edge_list: エッジ属性辞書のリスト / 空リストの場合、登録失敗
    Returns:
         list[dict]: 登録エッジ一覧
    """
    # 指定内容のどれかが登録済みなら、全て登録しない
    for edge in edge_list:
        node1_id, route1_id = edge["node1_id"], edge["route1_id"]
        node2_id, route2_id = edge["node2_id"], edge["route2_id"]
        if get_edge(G, node1_id, node2_id, route1_id=route1_id, route2_id=route2_id):
            raise ValueError(F"ERROR: 指定エッジは登録済:{node1_id=}\t{node2_id=}")
    # 各指定エッジの登録
    for edge in edge_list:
        node1_id, route1_id = edge["node1_id"], edge["route1_id"]
        node2_id, route2_id = edge["node2_id"], edge["route2_id"]
        edge_id = edge["edge_id"]
        add_edge(G, node1_id, node2_id, route1_id=route1_id, route2_id=route2_id, edge_id=edge_id)
    return query_edges(G)


# noinspection PyPep8Naming,PyTypeChecker
def update_edge_attrs(G: nx.MultiGraph, node1_id: int, node2_id: int, *, route1_id: int, route2_id: int,
                      new_attrs: dict[str, str | int]) -> dict | None:
    """エッジの属性を更新する。

    Args:
        G (nx.MultiGraph): 対象グラフ
        node1_id: 始点ノードID
        node2_id: 終点ノードID
        route1_id: 始点ルートID
        route2_id: 終点ルートID
        new_attrs: 追加・更新属性
    Returns:
        dict: 更新後のエッジ属性辞書 / None:更新失敗
    """
    # 指定ノードが見つかれば、属性を更新する
    if get_edge(G, node1_id, node2_id, route1_id=route1_id, route2_id=route2_id) is not None:
        key = _generate_edge_key(node1_id, node2_id, route1_id=route1_id, route2_id=route2_id)
        G.edges[node1_id, node2_id, key].update(new_attrs)
        return get_edge(G, node1_id, node2_id, route1_id=route1_id, route2_id=route2_id)
    return None


# noinspection PyPep8Naming
def get_shortest_path(G: nx.MultiGraph, node1_id: int, node2_id: int) -> list[int]:
    """指定ノード間の最短パスを取得

    Args:
        G (nx.MultiGraph): 対象グラフ
        node1_id (int): 開始ノードID
        node2_id (int): 終了ノードID
    Returns:
        list[int]: 最短パス（パスが存在しない場合 空リストを返す）
    """
    try:
        res = nx.shortest_path(G, source=node1_id, target=node2_id)
    except nx.NetworkXNoPath:
        res = []
    return res


# noinspection PyPep8Naming
def get_simple_path(G: nx.MultiGraph, node1_id: int, node2_id: int) -> list[list[int]]:
    """指定されたノード間の全接続パスを取得する
    指定ノードに複数のパスが存在する場合の戻り値の例: 下記の例では3つのパスが存在し、そのノードIDをそれぞれのリストで示している
       例: get_simple_path(G, 1,6)=[[1, 5, 6], [1, 2, 3, 4, 5, 6], [1, 9, 8, 7, 6]]

    Args:
        G (nx.MultiGraph): 対象グラフ
        node1_id (int): 開始ノードID
        node2_id (int): 終了ノードID
    Returns:
        list[list[int]]: 見つかった全パスをノードIDリストで返す（パスが存在しない場合 空リスト）
    """
    try:
        paths = list(nx.all_simple_paths(G, source=node1_id, target=node2_id))
        # 重複するリスト要素を除外
        res = [list(t) for t in set(tuple(sub_path) for sub_path in paths)]
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        res = 0
    return res


# noinspection PyPep8Naming
def verify_path(G: nx.MultiGraph, path: list[int]) -> bool:
    """指定されたノード列が有効パスかを検証する。

    Args:
        G (nx.MultiGraph): 対象グラフ
        path (list[int]): ノードIDの順列（開始→中間→終了）
    Returns:
        bool: パスが存在すれば True、存在しなければ False
    """
    # path[i] と path[i+1] の間にエッジが存在するかを逐次確認し、存在しない場合は False を返す。
    for i in range(len(path) - 1):
        if not G.has_edge(path[i], path[i + 1]):
            return False
    return True
