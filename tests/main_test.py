import pytest
from src.main import LogAnalyzer
import os


curr_dir = os.path.dirname(__file__)
file_path = os.path.join(curr_dir, "test_logs.txt")
log_analyzer = LogAnalyzer(file_path)

class TestParseLine:
    def test_parse_line(self):
        line = '178.252.142.2 - - [22/Jan/2019:15:06:49 +0330] "GET /image/63272/productModel/150x150 HTTP/1.1" 200 4275 "https://www.zanbil.ir/browse/digital-camera/%D8%AF%D9%88%D8%B1%D8%A8%DB%8C%D9%86-%D8%B9%DA%A9%D8%A7%D8%B3%DB%8C" "Mozilla/5.0 (Windows NT 6.1; rv:64.0) Gecko/20100101 Firefox/64.0" "-"'
        log_dict = log_analyzer.parse_line(line)

        assert log_dict['ip'] == '178.252.142.2'
        assert log_dict['timestamp'] == '22/Jan/2019:15:06:49'
        assert log_dict['method'] == 'GET'
        assert log_dict['path'] == '/image/63272/productModel/150x150'
        assert log_dict['status'] == 200
        assert log_dict['size'] == 4275

    def test_parse_error_query(self):
        line = '207.46.13.136 - - [22/Jan/2019:03:56:19 +0330] "GET /product/14926 HTTP/1.1" 404 33617 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)" "-"'
        log_dict = log_analyzer.parse_line(line)

        assert log_dict['status'] == 404
        assert log_dict['size'] == 33617

    def test_long_path(self):
        path = '/rapidGrails/jsonList?maxColumns=16&domainClass=eshop.Order&filter=[{op:%27inSession%27,%20field:%27id%27,%20val:%27orderList718ed343d0b041caa513d7585bee355e%27}]&columns=[{%27name%27:%27trackingCode%27,%27width%27:110},{%27name%27:%27ownerName%27,%27width%27:120},{%27name%27:%27productsName%27,%27width%27:320,%27sortable%27:false},{%27name%27:%27ownerMobile%27,%27width%27:110},{%27name%27:%27deliveryMethodName%27,%27width%27:120,%27sortable%27:false},{%27name%27:%27deliveryCityName%27,%27width%27:120,%27sortable%27:false},{%27name%27:%27addressRegionName%27,%27width%27:120,%27sortable%27:false},{%27name%27:%27courier%27,%27width%27:120,%27expression%27:%27obj[\x5C%27courier\x5C%27]?.fullName%27},{%27name%27:%27status%27,%27width%27:110},{%27name%27:%27invoiceType%27,%27width%27:60,%27expression%27:%27g.message(code:%20obj[\x5C%27invoiceTypeCode\x5C%27])%27},{%27name%27:%27itemsDeliveryStatus%27,%27width%27:60},{%27name%27:%27creationType%27,%27width%27:50},{%27name%27:%27creationMedia%27,%27width%27:50},{%27name%27:%27completionMedia%27,%27width%27:50},{%27name%27:%27completionFollower%27,%27width%27:120},{%27name%27:%27lastActionDate%27,%27width%27:100,%27expression%27:%27rg.formatJalaliDate(date:%20%20obj[\x5C%27lastActionDate\x5C%27],%20hm:\x5C%27true\x5C%27%20)%27}]&_search=false&nd=1548232773683&rows=10&page=2&sidx=lastActionDate&sord=desc'
        line = '151.239.241.163 - - [23/Jan/2019:12:05:58 +0330] "GET ' + path + ' HTTP/1.1" 200 1250 "https://www.zanbil.ir/orderAdministration/console/187598" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0" "-"'
        log_dict = log_analyzer.parse_line(line)

        assert log_dict['path'] == path
        assert len(path) > 1000

    def test_parse_line_with_large_size(self):
        line = '178.252.142.2 - - [22/Jan/2019:15:06:49 +0330] "GET /image/63272/productModel/150x150 HTTP/1.1" 200 4275222875'
        log_dict = log_analyzer.parse_line(line)

        assert log_dict['size'] == 4275222875


class TestParseLineInvalidLine:
    def test_parse_line_with_invalid_field(self):
        line = '178.252.142.2 - - [22/Jan/2019:15:06:49 +0330] "GET /image/63272/productModel/150x150 HTTP/1.1" 200 "https://www.zanbil.ir/browse/digital-camera/%D8%AF%D9%88%D8%B1%D8%A8%DB%8C%D9%86-%D8%B9%DA%A9%D8%A7%D8%B3%DB%8C"'

        with pytest.raises(ValueError):
            log_analyzer.parse_line(line)

    def test_parse_incomplete_line(self):
        line = '178.252.142.2 - - [22/Jan/2019:15:06:49 +0330] "GET /image/63272/productModel/150x150 HTTP/1.1" 200'

        with pytest.raises(IndexError):
            log_analyzer.parse_line(line)

    def test_parse_line_with_invalid_status(self):
        line = '178.252.142.2 - - [22/Jan/2019:15:06:49 +0330] "GET /image/63272/productModel/150x150 HTTP/1.1" twenty 4812'

        with pytest.raises(ValueError):
            log_analyzer.parse_line(line)


class TestParseLineParametrized:
    @pytest.mark.parametrize("val,expected_ip,expected_timestamp,expected_method", [
        ('178.252.142.2 - - [22/Jan/2019:15:06:49 +0330] "GET /image/63272/productModel/150x150 HTTP/1.1" 200 4275',
         '178.252.142.2', '22/Jan/2019:15:06:49', 'GET'),
        ('207.46.13.136 - - [22/Jan/2019:03:56:19 +0330] "GET /product/14926 HTTP/1.1" 404 33617',
         '207.46.13.136', '22/Jan/2019:03:56:19', 'GET'),
        ('91.98.155.28 - - [23/Jan/2019:12:06:02 +0330] "POST /ajaxFilter/p51?page=6 HTTP/1.1" 200 7097',
         '91.98.155.28', '23/Jan/2019:12:06:02', 'POST'),
    ])
    def test_parse_line_parametrize(self, val, expected_ip, expected_timestamp, expected_method):
        log_dict = log_analyzer.parse_line(val)

        assert log_dict['ip'] == expected_ip
        assert log_dict['timestamp'] == expected_timestamp
        assert log_dict['method'] == expected_method

    @pytest.mark.parametrize("size", [0, 1, 14, 2345, 3685322, 883109019])
    def test_various_size_parse(self, size):
        line = f'91.98.155.28 - - [23/Jan/2019:12:06:02 +0330] "POST /ajaxFilter/p51?page=6 HTTP/1.1" 200 {size}'
        log_dict = log_analyzer.parse_line(line)

        assert log_dict['size'] == size


class TestGetTopIP:
    def test_get_top_ip(self):
        analyzer = LogAnalyzer(file_path)
        top_ip_list = analyzer.get_top_ips(2)

        assert top_ip_list[0] == '91.98.155.28'
        assert top_ip_list[1] == '91.98.125.28'


class TestErrorRate:
    def test_get_error_rate(self):
        analyzer = LogAnalyzer(file_path)
        rate = analyzer.get_error_rate()

        assert rate == (3 / 7)


class TestGetMostPopularPages:
    def test_get_most_popular_pages(self):
        analyzer = LogAnalyzer(file_path)
        top_pages = analyzer.get_most_popular_pages(3)

        assert top_pages[0] == '/image/59771/clock/100x100'
        assert top_pages[1] == '/image/59771/granat/100x100'
        assert top_pages[2] == '/image/59771/pingpong/100x100'

class TestGetHourlyDistribution:
    def test_get_hourly_distribution(self):
        analyzer = LogAnalyzer(file_path)
        hourly_distribution = analyzer.get_hourly_distribution()

        assert hourly_distribution[12] == 3
        assert hourly_distribution[10] == 2
        assert hourly_distribution[13] == 1
        assert hourly_distribution[1] == 1