from collections import defaultdict
import json
import threading
import Queue
import urllib3


class Node(object):
    def __init__(self, node_id):
        self.secret = None
        self.children = []
        self.node_id = node_id


class CurbsideQuery(object):
    def __init__(self):
        self.http = urllib3.HTTPConnectionPool(
            'challenge.curbside.com', maxsize=100)
        resp = self.http.request('GET', '/get-session')
        self.session = json.loads(resp.data)['session']

    def fetch_node(self, node):
        return self._fetch_data(node)

    def fetch_roots(self):
        return self._fetch_data('start')['next']

    def _fetch_data(self, path):
        resp = self.http.request('GET', '/%s' % path,
                                 headers={'session': self.session})
        if resp.status != 200:
            raise RuntimeError('Failed to query: %s' % resp.data)
        return json.loads(resp.data)


def worker(q, visited, levels, update_lock, cs_query):
    while True:
        node = q.get()
        if not node:
            q.task_done()
            return
        with update_lock:
            if node not in visited:
                visited.add(node)
            else:
                q.task_done()
                continue
        data = cs_query.fetch_node(node)
        normalized = dict((k.lower(), v) for k, v in data.items())
        if 'next' in normalized:
            if type(normalized['next']) == list:
                for n in normalized['next']:
                    q.put(n)
            else:
                q.put(normalized['next'])
        with update_lock:
            levels[int(normalized['depth'])].append(normalized)
        q.task_done()


def query_tree():
    cs_query = CurbsideQuery()
    start_nodes = cs_query.fetch_roots()
    visited = set()
    levels = defaultdict(list)

    threads = []
    update_lock = threading.Lock()
    q = Queue.Queue()
    levels[0] = start_nodes
    for node in start_nodes:
        q.put(node)

    for i in range(10):
        t = threading.Thread(
            target=worker, args=(q, visited, levels, update_lock, cs_query))
        t.start()
        threads.append(t)
    q.join()
    for _ in threads:
        q.put(None)
    q.join()
    for t in threads:
        t.join()
    return levels


def build_tree(levels):
    roots = [Node(node_id) for node_id in levels[0]]
    cur_level = roots
    for i in range(1, len(levels.keys())):
        lvl = levels[i]
        for entry in lvl:
            for node in cur_level:
                if node.node_id == entry['id']:
                    if 'next' in entry:
                        if type(entry['next']) == list:
                            node.children.extend(
                                [Node(node_id) for node_id in entry['next']])
                        else:
                            node.children.append(Node(entry['next']))
                    elif 'secret' in entry:
                        node.secret = entry['secret']
        cur_level = reduce(lambda x, y: x + y.children, cur_level, [])
    return roots


def get_secret(roots):
    secrets = ''
    for root in roots:
        if root.secret:
            secrets += root.secret
        if not root.children:
            continue
        if root.children:
            for c in root.children:
                secrets += get_secret([c])
    return secrets


levels = query_tree()
tree = build_tree(levels)
print get_secret(tree)
