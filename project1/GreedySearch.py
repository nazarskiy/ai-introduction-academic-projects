from search_algorithm_abs import CSearchAlg
import heapq

class CGreedySearch(CSearchAlg):
    def solve_maze(self):
        if self.m_s == self.m_e:
            self.viz(0, [])
            return
        self.viz(-1, [])

        pr_q = []
        heapq.heappush(pr_q, (0, self.m_s))

        self.m_s.set_status("open")
        self.m_s.set_d(0)
        self.m_s.set_h(self.m_e)

        while pr_q:
            _, v = heapq.heappop(pr_q)
            curr_path = self.m_maze.uvpath(self.m_s, v)

            for coord in v.neighbours(self.m_maze.m_m, self.m_maze.m_n):
                w = self.m_maze.m_Maze[coord[0]][coord[1]]
                if w.get_status() == "not_found" and w.get_value() != 'X':
                    w.set_h(self.m_e)
                    heapq.heappush(pr_q, (w.get_h(), w))
                    w.set_status("open")
                    self.m_expanded += 1
                    w.set_d(v.get_d() + 1)
                    w.set_p(v)
                    if w != self.m_e:
                        w.set_value('#')
                    self.viz(self.m_e.get_d(), curr_path)
                    if w == self.m_e:
                        pr_q.clear()
                        break
            v.set_status("closed")