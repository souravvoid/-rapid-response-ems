import heapq
import math
from datetime import datetime, timedelta

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c  # in km

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}  # node -> list of (neighbor, weight)

    def add_node(self, node):
        self.nodes.add(node)
        self.edges.setdefault(node, [])

    def add_edge(self, a, b, weight):
        self.edges.setdefault(a, []).append((b, weight))
        self.edges.setdefault(b, []).append((a, weight))

    def dijkstra(self, start, end):
        pq = [(0, start)]
        dist = {node: float('inf') for node in self.nodes}
        prev = {node: None for node in self.nodes}
        dist[start] = 0

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            if u == end:
                break
            for v, w in self.edges.get(u, []):
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))

        if dist[end] == float('inf'):
            return None, []
        # reconstruct path
        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return dist[end], path

def build_graph_from_points(ambulances, hospitals, incident_point):
    """
    Build a simple graph where nodes are ambulances, hospitals, and 'INCIDENT'.
    Edges weights = haversine distance (km).
    """
    g = Graph()
    # create node ids
    for amb in ambulances:
        nid = f"AMB-{amb.id}"
        g.add_node(nid)
    for hosp in hospitals:
        nid = f"HOSP-{hosp.id}"
        g.add_node(nid)
    g.add_node("INCIDENT")

    # connect AMBs <-> INCIDENT and AMBs <-> HOSP, HOSP <-> INCIDENT
    for amb in ambulances:
        amb_node = f"AMB-{amb.id}"
        d = haversine(amb.current_latitude, amb.current_longitude, incident_point[0], incident_point[1])
        g.add_edge(amb_node, "INCIDENT", d)
        for hosp in hospitals:
            hosp_node = f"HOSP-{hosp.id}"
            d2 = haversine(amb.current_latitude, amb.current_longitude, hosp.latitude, hosp.longitude)
            g.add_edge(amb_node, hosp_node, d2)

    for hosp in hospitals:
        hosp_node = f"HOSP-{hosp.id}"
        d3 = haversine(hosp.latitude, hosp.longitude, incident_point[0], incident_point[1])
        g.add_edge(hosp_node, "INCIDENT", d3)

    return g

def estimate_eta_from_distance_km(distance_km, avg_speed_kmph=40):
    hours = distance_km / avg_speed_kmph
    minutes = int(hours * 60)
    eta_dt = datetime.utcnow() + timedelta(minutes=minutes)
    return eta_dt.isoformat()
