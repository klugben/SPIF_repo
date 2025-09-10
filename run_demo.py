#!/usr/bin/env python3
"""
AkMon 演示脚本
用于验证 app.py 的基本功能
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from src.akmon.app import AkMonApp


def main():
    """主函数"""
    print("🚀 启动 AkMon 演示")
    print("=" * 50)
    
    try:
        # 创建应用实例
        app = AkMonApp()
        
        # 运行单次检查
        print("📊 执行单次数据检查...")
        result = app.run_single_check()
        
        if 'error' in result:
            print(f"❌ 检查失败: {result['error']}")
            return False
        
        print("✅ 检查完成!")
        
        # 显示结果摘要
        basis_data = result['basis_data']
        alert_result = result['alert_result']
        
        print(f"\n📈 数据摘要:")
        print(f"   合约: {basis_data['contract_code']}")
        print(f"   基差: {basis_data['basis_value']:.2f}")
        print(f"   贴水率: {basis_data['carry_rate']:.2f}%")
        
        if alert_result['alert_triggered']:
            print(f"⚠️  预警状态: 已触发")
            for alert in alert_result['alerts']:
                print(f"   - {alert['message']}")
        else:
            print(f"✅ 预警状态: 未触发")
        
        print("\n🎉 演示完成!")
        return True
        
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
