from collections import Counter


class LogAnalyzer:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.logs = []
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    self.logs.append(self.parse_line(line))
                except (ValueError, IndexError) as e:
                    print(f"Invalid line. Error: {e}")
                    continue

    def parse_line(self, line: str) -> dict:
        parsed = line.split()

        return {
            'ip': parsed[0],
            'timestamp': parsed[3][1:],
            'method': parsed[5][1:],
            'path': parsed[6],
            'status': int(parsed[8]),
            'size': int(parsed[9])
        }

    def get_top_ips(self, n: int = 10) -> list:
        ip_cnt = Counter(log['ip'] for log in self.logs)
        return [ip for ip, _ in ip_cnt.most_common(n)]

    def get_error_rate(self) -> float:
        if not self.logs:
            return 0.0
        error_query_cnt = len([pair['status'] for pair in self.logs if pair['status'] >= 400])
        lines_in_file_cnt = len(self.logs)
        return error_query_cnt / lines_in_file_cnt

    def get_most_popular_pages(self, n: int = 10) -> list:
        page_cnt = Counter(log['path'] for log in self.logs)
        return list(page for page, _ in page_cnt.most_common(n))

    def get_hourly_distribution(self) -> dict:
         times_cnt = Counter()
         for log in self.logs:
             hour = int(log['timestamp'].split(':')[1])
             times_cnt[hour] += 1
         return dict(sorted(times_cnt.items()))