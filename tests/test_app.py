"""
AkMon 应用测试用例
"""

import pytest
import sys
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.akmon.app import AkMonApp, Config, BasisData, AlertThreshold


class TestConfig:
    """配置模型测试"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = Config()
        assert config.timezone == "Asia/Shanghai"
        assert config.symbols == []
        assert config.scheduler == {}
        assert config.notifier == {}
        assert config.storage == {}
    
    def test_config_with_data(self):
        """测试带数据的配置"""
        config_data = {
            'timezone': 'UTC',
            'symbols': [{'type': 'future', 'code': 'IC'}],
            'scheduler': {'interval_seconds': 60},
            'notifier': {'type': 'wecom'},
            'storage': {'type': 'sqlite'}
        }
        config = Config(**config_data)
        assert config.timezone == 'UTC'
        assert len(config.symbols) == 1
        assert config.scheduler['interval_seconds'] == 60


class TestBasisData:
    """基差数据模型测试"""
    
    def test_basis_data_creation(self):
        """测试基差数据创建"""
        data = BasisData(
            contract_code="IC2509",
            trade_date=datetime.now(),
            open_price=4500.0,
            high_price=4520.0,
            low_price=4480.0,
            close_price=4510.0,
            volume=10000,
            amount=45100000.0,
            basis_value=-23.4,
            carry_rate=-0.52
        )
        assert data.contract_code == "IC2509"
        assert data.basis_value == -23.4
        assert data.carry_rate == -0.52


class TestAlertThreshold:
    """预警阈值模型测试"""
    
    def test_default_threshold(self):
        """测试默认阈值"""
        threshold = AlertThreshold()
        assert threshold.basis_threshold is None
        assert threshold.carry_rate_threshold is None
        assert threshold.trigger_direction == "below"
    
    def test_threshold_with_values(self):
        """测试带值的阈值"""
        threshold = AlertThreshold(
            basis_threshold=-30.0,
            carry_rate_threshold=-1.0,
            trigger_direction="above"
        )
        assert threshold.basis_threshold == -30.0
        assert threshold.carry_rate_threshold == -1.0
        assert threshold.trigger_direction == "above"


class TestAkMonApp:
    """AkMon应用测试"""
    
    @patch('src.akmon.app.yaml.safe_load')
    @patch('builtins.open')
    def test_load_config_success(self, mock_open, mock_yaml_load):
        """测试成功加载配置"""
        mock_yaml_load.return_value = {
            'timezone': 'Asia/Shanghai',
            'symbols': [{'type': 'future', 'code': 'IC'}]
        }
        
        app = AkMonApp()
        assert app.config.timezone == 'Asia/Shanghai'
        assert len(app.config.symbols) == 1
    
    @patch('src.akmon.app.yaml.safe_load')
    @patch('builtins.open')
    def test_load_config_file_not_found(self, mock_open, mock_yaml_load):
        """测试配置文件不存在"""
        mock_open.side_effect = FileNotFoundError()
        
        app = AkMonApp()
        assert app.config.timezone == "Asia/Shanghai"  # 默认值
    
    @patch('src.akmon.app.ak.futures_zh_spot')
    def test_get_ic_future_data_success(self, mock_futures):
        """测试成功获取期货数据"""
        import pandas as pd
        
        # 模拟返回数据
        mock_data = pd.DataFrame({
            '代码': ['IC2509', 'IF2412'],
            '开盘价': [4500.0, 3200.0],
            '最高价': [4520.0, 3220.0],
            '最低价': [4480.0, 3180.0],
            '最新价': [4510.0, 3210.0],
            '成交量': [10000, 8000],
            '成交额': [45100000.0, 25680000.0]
        })
        mock_futures.return_value = mock_data
        
        app = AkMonApp()
        result = app.get_ic_future_data("IC2509")
        
        assert result is not None
        assert result['contract_code'] == "IC2509"
        assert result['close_price'] == 4510.0
    
    @patch('src.akmon.app.ak.futures_zh_spot')
    def test_get_ic_future_data_not_found(self, mock_futures):
        """测试期货数据未找到"""
        import pandas as pd
        
        # 模拟空数据
        mock_data = pd.DataFrame({
            '代码': ['IF2412'],
            '开盘价': [3200.0],
            '最高价': [3220.0],
            '最低价': [3180.0],
            '最新价': [3210.0],
            '成交量': [8000],
            '成交额': [25680000.0]
        })
        mock_futures.return_value = mock_data
        
        app = AkMonApp()
        result = app.get_ic_future_data("IC2509")
        
        assert result is None
    
    @patch('src.akmon.app.ak.stock_zh_index_daily')
    def test_get_cs500_index_data_success(self, mock_index):
        """测试成功获取指数数据"""
        import pandas as pd
        
        # 模拟返回数据
        mock_data = pd.DataFrame({
            'close': [5000.0, 5010.0]
        })
        mock_index.return_value = mock_data
        
        app = AkMonApp()
        result = app.get_cs500_index_data()
        
        assert result is not None
        assert result == 5010.0
    
    @patch('src.akmon.app.ak.stock_zh_index_daily')
    def test_get_cs500_index_data_empty(self, mock_index):
        """测试指数数据为空"""
        import pandas as pd
        
        # 模拟空数据
        mock_data = pd.DataFrame()
        mock_index.return_value = mock_data
        
        app = AkMonApp()
        result = app.get_cs500_index_data()
        
        assert result is None
    
    def test_calculate_basis_indicator(self):
        """测试基差指标计算"""
        app = AkMonApp()
        
        future_data = {
            'contract_code': 'IC2509',
            'trade_date': datetime.now(),
            'open_price': 4500.0,
            'high_price': 4520.0,
            'low_price': 4480.0,
            'close_price': 4510.0,
            'volume': 10000,
            'amount': 45100000.0
        }
        index_price = 5000.0
        
        result = app.calculate_basis_indicator(future_data, index_price)
        
        assert isinstance(result, BasisData)
        assert result.basis_value == 4510.0 - 5000.0  # -490.0
        assert result.carry_rate == pytest.approx(-490.0 / 5000.0 * 100, rel=1e-3)
    
    def test_check_threshold_alert_below_basis(self):
        """测试基差下穿预警"""
        app = AkMonApp()
        
        basis_data = BasisData(
            contract_code="IC2509",
            trade_date=datetime.now(),
            open_price=4500.0,
            high_price=4520.0,
            low_price=4480.0,
            close_price=4510.0,
            volume=10000,
            amount=45100000.0,
            basis_value=-500.0,  # 低于阈值
            carry_rate=-10.0
        )
        
        threshold = AlertThreshold(
            basis_threshold=-30.0,
            trigger_direction="below"
        )
        
        result = app.check_threshold_alert(basis_data, threshold)
        
        assert result['alert_triggered'] is True
        assert len(result['alerts']) == 1
        assert result['alerts'][0]['type'] == 'basis'
    
    def test_check_threshold_alert_above_carry_rate(self):
        """测试贴水率上穿预警"""
        app = AkMonApp()
        
        basis_data = BasisData(
            contract_code="IC2509",
            trade_date=datetime.now(),
            open_price=4500.0,
            high_price=4520.0,
            low_price=4480.0,
            close_price=4510.0,
            volume=10000,
            amount=45100000.0,
            basis_value=-20.0,
            carry_rate=5.0  # 高于阈值
        )
        
        threshold = AlertThreshold(
            carry_rate_threshold=1.0,
            trigger_direction="above"
        )
        
        result = app.check_threshold_alert(basis_data, threshold)
        
        assert result['alert_triggered'] is True
        assert len(result['alerts']) == 1
        assert result['alerts'][0]['type'] == 'carry_rate'
    
    def test_check_threshold_alert_no_trigger(self):
        """测试未触发预警"""
        app = AkMonApp()
        
        basis_data = BasisData(
            contract_code="IC2509",
            trade_date=datetime.now(),
            open_price=4500.0,
            high_price=4520.0,
            low_price=4480.0,
            close_price=4510.0,
            volume=10000,
            amount=45100000.0,
            basis_value=-20.0,  # 高于阈值-30.0
            carry_rate=-0.5  # 高于阈值-1.0
        )
        
        threshold = AlertThreshold(
            basis_threshold=-30.0,
            carry_rate_threshold=-1.0,
            trigger_direction="below"
        )
        
        result = app.check_threshold_alert(basis_data, threshold)
        
        assert result['alert_triggered'] is False
        assert len(result['alerts']) == 0
    
    def test_check_threshold_alert_boundary_values(self):
        """测试边界值检查"""
        app = AkMonApp()
        
        # 测试等于阈值的情况（不应触发）
        basis_data = BasisData(
            contract_code="IC2509",
            trade_date=datetime.now(),
            open_price=4500.0,
            high_price=4520.0,
            low_price=4480.0,
            close_price=4510.0,
            volume=10000,
            amount=45100000.0,
            basis_value=-30.0,  # 等于阈值
            carry_rate=-1.0  # 等于阈值
        )
        
        threshold = AlertThreshold(
            basis_threshold=-30.0,
            carry_rate_threshold=-1.0,
            trigger_direction="below"
        )
        
        result = app.check_threshold_alert(basis_data, threshold)
        
        # 等于阈值不应触发预警
        assert result['alert_triggered'] is False
    
    @patch('src.akmon.app.AkMonApp.get_ic_future_data')
    @patch('src.akmon.app.AkMonApp.get_cs500_index_data')
    def test_run_single_check_success(self, mock_index, mock_future):
        """测试成功执行单次检查"""
        app = AkMonApp()
        
        # 模拟期货数据
        mock_future.return_value = {
            'contract_code': 'IC2509',
            'trade_date': datetime.now(),
            'open_price': 4500.0,
            'high_price': 4520.0,
            'low_price': 4480.0,
            'close_price': 4510.0,
            'volume': 10000,
            'amount': 45100000.0
        }
        
        # 模拟指数数据
        mock_index.return_value = 5000.0
        
        result = app.run_single_check()
        
        assert 'error' not in result
        assert 'basis_data' in result
        assert 'alert_result' in result
        assert result['basis_data']['basis_value'] == -490.0
    
    @patch('src.akmon.app.AkMonApp.get_ic_future_data')
    def test_run_single_check_future_data_failed(self, mock_future):
        """测试期货数据获取失败"""
        app = AkMonApp()
        
        # 模拟期货数据获取失败
        mock_future.return_value = None
        
        result = app.run_single_check()
        
        assert 'error' in result
        assert result['error'] == '获取期货数据失败'
    
    @patch('src.akmon.app.AkMonApp.get_ic_future_data')
    @patch('src.akmon.app.AkMonApp.get_cs500_index_data')
    def test_run_single_check_index_data_failed(self, mock_index, mock_future):
        """测试指数数据获取失败"""
        app = AkMonApp()
        
        # 模拟期货数据成功
        mock_future.return_value = {
            'contract_code': 'IC2509',
            'trade_date': datetime.now(),
            'open_price': 4500.0,
            'high_price': 4520.0,
            'low_price': 4480.0,
            'close_price': 4510.0,
            'volume': 10000,
            'amount': 45100000.0
        }
        
        # 模拟指数数据失败
        mock_index.return_value = None
        
        result = app.run_single_check()
        
        assert 'error' in result
        assert result['error'] == '获取指数数据失败'


class TestIntegration:
    """集成测试"""
    
    @patch('src.akmon.app.ak.futures_zh_spot')
    @patch('src.akmon.app.ak.stock_zh_index_daily')
    def test_full_workflow(self, mock_index, mock_futures):
        """测试完整工作流程"""
        import pandas as pd
        
        # 模拟期货数据
        mock_futures.return_value = pd.DataFrame({
            '代码': ['IC2509'],
            '开盘价': [4500.0],
            '最高价': [4520.0],
            '最低价': [4480.0],
            '最新价': [4510.0],
            '成交量': [10000],
            '成交额': [45100000.0]
        })
        
        # 模拟指数数据
        mock_index.return_value = pd.DataFrame({
            'close': [5000.0, 5010.0]
        })
        
        app = AkMonApp()
        result = app.run_single_check()
        
        # 验证结果
        assert 'error' not in result
        assert result['basis_data']['contract_code'] == 'IC2509'
        assert result['basis_data']['basis_value'] == -490.0
        assert 'alert_result' in result
        assert 'alert_triggered' in result['alert_result']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
