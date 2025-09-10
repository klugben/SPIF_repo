"""
AkMon - AkShare驱动的期货监控与提醒系统
主应用入口文件
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

import akshare as ak
import yaml
from pydantic import BaseModel, Field


class Config(BaseModel):
    """应用配置模型"""
    timezone: str = "Asia/Shanghai"
    symbols: list = Field(default_factory=list)
    scheduler: Dict[str, Any] = Field(default_factory=dict)
    notifier: Dict[str, Any] = Field(default_factory=dict)
    storage: Dict[str, Any] = Field(default_factory=dict)


class BasisData(BaseModel):
    """基差数据模型"""
    contract_code: str
    trade_date: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    amount: float
    basis_value: float
    carry_rate: float


class AlertThreshold(BaseModel):
    """预警阈值模型"""
    basis_threshold: Optional[float] = None
    carry_rate_threshold: Optional[float] = None
    trigger_direction: str = "below"  # above/below


class AkMonApp:
    """AkMon主应用类"""
    
    def __init__(self, config_path: str = "configs/app.yaml"):
        """
        初始化应用
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self, config_path: str) -> Config:
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            Config: 配置对象
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            return Config(**config_data)
        except FileNotFoundError:
            self.logger.warning(f"配置文件 {config_path} 不存在，使用默认配置")
            return Config()
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {e}")
            sys.exit(1)
    
    def _setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('akmon.log', encoding='utf-8')
            ]
        )
    
    def get_ic_future_data(self, contract_code: str = "IC2509") -> Optional[Dict[str, Any]]:
        """
        获取IC期货数据
        
        Args:
            contract_code: 合约代码
            
        Returns:
            Optional[Dict[str, Any]]: 期货数据字典
        """
        try:
            # 获取期货实时行情数据
            df = ak.futures_zh_spot()
            
            # 筛选IC合约数据
            ic_data = df[df['代码'] == contract_code]
            
            if ic_data.empty:
                self.logger.warning(f"未找到合约 {contract_code} 的数据")
                return None
            
            # 获取最新数据
            latest_data = ic_data.iloc[-1]
            
            return {
                'contract_code': contract_code,
                'trade_date': datetime.now(),
                'open_price': float(latest_data['开盘价']),
                'high_price': float(latest_data['最高价']),
                'low_price': float(latest_data['最低价']),
                'close_price': float(latest_data['最新价']),
                'volume': int(latest_data['成交量']),
                'amount': float(latest_data['成交额'])
            }
            
        except Exception as e:
            self.logger.error(f"获取IC期货数据失败: {e}")
            return None
    
    def get_cs500_index_data(self) -> Optional[float]:
        """
        获取中证500指数数据
        
        Returns:
            Optional[float]: 中证500指数价格
        """
        try:
            # 获取中证500指数数据
            df = ak.stock_zh_index_daily(symbol="sh000905")
            
            if df.empty:
                self.logger.warning("未找到中证500指数数据")
                return None
            
            # 获取最新数据
            latest_data = df.iloc[-1]
            return float(latest_data['close'])
            
        except Exception as e:
            self.logger.error(f"获取中证500指数数据失败: {e}")
            return None
    
    def calculate_basis_indicator(self, future_data: Dict[str, Any], index_price: float) -> BasisData:
        """
        计算基差指标
        
        Args:
            future_data: 期货数据
            index_price: 指数价格
            
        Returns:
            BasisData: 基差数据
        """
        # 计算基差 = 期货价格 - 指数价格
        basis_value = future_data['close_price'] - index_price
        
        # 计算贴水率 = (期货价格 - 指数价格) / 指数价格 * 100%
        carry_rate = (basis_value / index_price) * 100 if index_price > 0 else 0
        
        return BasisData(
            contract_code=future_data['contract_code'],
            trade_date=future_data['trade_date'],
            open_price=future_data['open_price'],
            high_price=future_data['high_price'],
            low_price=future_data['low_price'],
            close_price=future_data['close_price'],
            volume=future_data['volume'],
            amount=future_data['amount'],
            basis_value=basis_value,
            carry_rate=carry_rate
        )
    
    def check_threshold_alert(self, basis_data: BasisData, threshold: AlertThreshold) -> Dict[str, Any]:
        """
        检查阈值预警
        
        Args:
            basis_data: 基差数据
            threshold: 预警阈值
            
        Returns:
            Dict[str, Any]: 预警结果
        """
        alerts = []
        
        # 检查基差阈值
        if threshold.basis_threshold is not None:
            if threshold.trigger_direction == "below":
                if basis_data.basis_value < threshold.basis_threshold:
                    alerts.append({
                        'type': 'basis',
                        'message': f"基差 {basis_data.basis_value:.2f} 低于阈值 {threshold.basis_threshold}",
                        'triggered': True
                    })
            else:  # above
                if basis_data.basis_value > threshold.basis_threshold:
                    alerts.append({
                        'type': 'basis',
                        'message': f"基差 {basis_data.basis_value:.2f} 高于阈值 {threshold.basis_threshold}",
                        'triggered': True
                    })
        
        # 检查贴水率阈值
        if threshold.carry_rate_threshold is not None:
            if threshold.trigger_direction == "below":
                if basis_data.carry_rate < threshold.carry_rate_threshold:
                    alerts.append({
                        'type': 'carry_rate',
                        'message': f"贴水率 {basis_data.carry_rate:.2f}% 低于阈值 {threshold.carry_rate_threshold}%",
                        'triggered': True
                    })
            else:  # above
                if basis_data.carry_rate > threshold.carry_rate_threshold:
                    alerts.append({
                        'type': 'carry_rate',
                        'message': f"贴水率 {basis_data.carry_rate:.2f}% 高于阈值 {threshold.carry_rate_threshold}%",
                        'triggered': True
                    })
        
        return {
            'contract_code': basis_data.contract_code,
            'timestamp': basis_data.trade_date,
            'basis_value': basis_data.basis_value,
            'carry_rate': basis_data.carry_rate,
            'alerts': alerts,
            'alert_triggered': len(alerts) > 0
        }
    
    def run_single_check(self, contract_code: str = "IC2509") -> Dict[str, Any]:
        """
        执行单次检查
        
        Args:
            contract_code: 合约代码
            
        Returns:
            Dict[str, Any]: 检查结果
        """
        self.logger.info(f"开始执行单次检查 - 合约: {contract_code}")
        
        # 获取期货数据
        future_data = self.get_ic_future_data(contract_code)
        if not future_data:
            return {'error': '获取期货数据失败'}
        
        # 获取指数数据
        index_price = self.get_cs500_index_data()
        if not index_price:
            return {'error': '获取指数数据失败'}
        
        # 计算基差指标
        basis_data = self.calculate_basis_indicator(future_data, index_price)
        
        # 设置默认阈值（从配置文件读取或使用默认值）
        threshold = AlertThreshold(
            basis_threshold=-30.0,  # 默认基差阈值
            carry_rate_threshold=-1.0,  # 默认贴水率阈值
            trigger_direction="below"
        )
        
        # 检查预警
        alert_result = self.check_threshold_alert(basis_data, threshold)
        
        # 输出结果到控制台
        self._console_output(basis_data, alert_result)
        
        return {
            'basis_data': basis_data.dict(),
            'alert_result': alert_result
        }
    
    def _console_output(self, basis_data: BasisData, alert_result: Dict[str, Any]):
        """
        控制台输出结果
        
        Args:
            basis_data: 基差数据
            alert_result: 预警结果
        """
        print("=" * 60)
        print(f"AkMon 监控结果 - {basis_data.contract_code}")
        print("=" * 60)
        print(f"时间: {basis_data.trade_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"期货价格: {basis_data.close_price:.2f}")
        print(f"基差: {basis_data.basis_value:.2f}")
        print(f"贴水率: {basis_data.carry_rate:.2f}%")
        print(f"成交量: {basis_data.volume:,}")
        print(f"成交额: {basis_data.amount:,.2f}")
        print("-" * 60)
        
        if alert_result['alert_triggered']:
            print("⚠️  预警触发!")
            for alert in alert_result['alerts']:
                print(f"   {alert['message']}")
        else:
            print("✅ 未触发预警")
        
        print("=" * 60)
    
    def run(self):
        """运行应用"""
        self.logger.info("启动 AkMon 应用")
        
        try:
            # 执行单次检查
            result = self.run_single_check()
            
            if 'error' in result:
                self.logger.error(f"检查失败: {result['error']}")
                return False
            
            self.logger.info("检查完成")
            return True
            
        except Exception as e:
            self.logger.error(f"应用运行失败: {e}")
            return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AkMon - AkShare驱动的期货监控与提醒系统')
    parser.add_argument('--config', '-c', default='configs/app.yaml', help='配置文件路径')
    parser.add_argument('--contract', default='IC2509', help='合约代码')
    
    args = parser.parse_args()
    
    # 创建应用实例
    app = AkMonApp(config_path=args.config)
    
    # 运行应用
    success = app.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
