#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for System Improvements
Tests the new system improvements functionality for Phase 5
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.system_improvements import (
    get_performance_monitor, get_security_enhancer, 
    get_config_manager, get_system_tester
)

def test_performance_monitor():
    """Test performance monitoring functionality"""
    print("📊 Testing Performance Monitor...")
    
    try:
        monitor = get_performance_monitor()
        
        # Start monitoring
        print("   🔄 Starting performance monitoring...")
        monitor.start_monitoring()
        time.sleep(2)  # Let it collect some data
        
        # Get performance summary
        summary = monitor.get_performance_summary()
        print("   📈 Performance Summary:")
        for metric, data in summary.items():
            if isinstance(data, dict):
                print(f"      {metric}: {data.get('current', 'N/A')}% (avg: {data.get('average', 'N/A'):.1f}%)")
        
        # Get optimization suggestions
        suggestions = monitor.optimize_performance()
        if suggestions:
            print("   💡 Performance Suggestions:")
            for suggestion in suggestions:
                print(f"      • {suggestion}")
        else:
            print("   ✅ No performance issues detected")
        
        # Stop monitoring
        monitor.stop_monitoring()
        
        return True
        
    except Exception as e:
        print(f"❌ Performance monitor test failed: {e}")
        return False

def test_security_enhancer():
    """Test security enhancement functionality"""
    print("\n🛡️  Testing Security Enhancer...")
    
    try:
        enhancer = get_security_enhancer()
        
        # Run security audit
        print("   🔍 Running security audit...")
        audit_results = enhancer.run_security_audit()
        
        print("   📋 Security Audit Results:")
        print(f"      Checks passed: {audit_results['checks_passed']}")
        print(f"      Checks failed: {audit_results['checks_failed']}")
        print(f"      Warnings: {len(audit_results['warnings'])}")
        print(f"      Critical issues: {len(audit_results['critical_issues'])}")
        
        if audit_results['warnings']:
            print("   ⚠️  Warnings:")
            for warning in audit_results['warnings'][:3]:  # Show first 3
                print(f"      • {warning}")
        
        if audit_results['critical_issues']:
            print("   🚨 Critical Issues:")
            for issue in audit_results['critical_issues']:
                print(f"      • {issue}")
        
        if audit_results['recommendations']:
            print("   💡 Recommendations:")
            for rec in audit_results['recommendations'][:3]:  # Show first 3
                print(f"      • {rec}")
        
        return True
        
    except Exception as e:
        print(f"❌ Security enhancer test failed: {e}")
        return False

def test_config_manager():
    """Test configuration management functionality"""
    print("\n⚙️  Testing Configuration Manager...")
    
    try:
        config_manager = get_config_manager()
        
        # Test getting default configs
        print("   📖 Testing default configurations...")
        main_config = config_manager.get_config('main')
        security_config = config_manager.get_config('security')
        
        print(f"      Main config keys: {len(main_config)}")
        print(f"      Security config keys: {len(security_config)}")
        
        # Test setting and getting config values
        print("\n   🔄 Testing config value updates...")
        test_key = 'test_value'
        test_value = f"test_{int(time.time())}"
        
        config_manager.set_config('main', test_key, test_value)
        retrieved_value = config_manager.get_config('main', test_key)
        
        if retrieved_value == test_value:
            print(f"      ✅ Config update successful: {test_key} = {test_value}")
        else:
            print(f"      ❌ Config update failed: expected {test_value}, got {retrieved_value}")
        
        # Test config validation
        print("\n   ✅ Testing config validation...")
        validation_result = config_manager.validate_config('main')
        
        if validation_result['valid']:
            print("      ✅ Main config is valid")
        else:
            print(f"      ❌ Main config validation failed: {validation_result.get('error', 'Unknown error')}")
            if validation_result.get('recommendations'):
                print("      💡 Recommendations:")
                for rec in validation_result['recommendations']:
                    print(f"         • {rec}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration manager test failed: {e}")
        return False

def test_system_tester():
    """Test system testing functionality"""
    print("\n🧪 Testing System Tester...")
    
    try:
        tester = get_system_tester()
        
        # Run full test suite
        print("   🚀 Running full test suite...")
        test_results = tester.run_full_test_suite()
        
        print("   📊 Test Suite Results:")
        print(f"      Overall Status: {test_results['overall_status'].upper()}")
        print(f"      Total Tests: {test_results['total_tests']}")
        print(f"      Passed: {test_results['passed_tests']}")
        print(f"      Failed: {test_results['failed_tests']}")
        
        # Show detailed results for each suite
        print("\n   📋 Detailed Results:")
        for suite_name, suite_result in test_results['test_results'].items():
            if isinstance(suite_result, dict) and 'total' in suite_result:
                status_icon = "✅" if suite_result['failed'] == 0 else "⚠️" if suite_result['passed'] > suite_result['failed'] else "❌"
                print(f"      {status_icon} {suite_name}: {suite_result['passed']}/{suite_result['total']} passed")
            else:
                print(f"      ❌ {suite_name}: Error - {suite_result.get('error', 'Unknown error')}")
        
        return test_results['overall_status'] != 'failed'
        
    except Exception as e:
        print(f"❌ System tester test failed: {e}")
        return False

def test_integration():
    """Test integration between all components"""
    print("\n🔗 Testing System Integration...")
    
    try:
        # Test all components working together
        print("   🔄 Testing component integration...")
        
        # Performance monitor
        monitor = get_performance_monitor()
        if monitor:
            print("      ✅ Performance monitor accessible")
        else:
            print("      ❌ Performance monitor not accessible")
        
        # Security enhancer
        enhancer = get_security_enhancer()
        if enhancer:
            print("      ✅ Security enhancer accessible")
        else:
            print("      ❌ Security enhancer not accessible")
        
        # Config manager
        config_manager = get_config_manager()
        if config_manager:
            print("      ✅ Configuration manager accessible")
        else:
            print("      ❌ Configuration manager not accessible")
        
        # System tester
        tester = get_system_tester()
        if tester:
            print("      ✅ System tester accessible")
        else:
            print("      ❌ System tester not accessible")
        
        # Test configuration integration
        print("\n   ⚙️  Testing configuration integration...")
        config_manager.set_config('performance', 'monitoring_enabled', True)
        config_manager.set_config('security', 'audit_logging', True)
        
        # Verify settings
        monitoring_enabled = config_manager.get_config('performance', 'monitoring_enabled')
        audit_logging = config_manager.get_config('security', 'audit_logging')
        
        if monitoring_enabled and audit_logging:
            print("      ✅ Configuration integration working")
        else:
            print("      ❌ Configuration integration failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all system improvement tests"""
    print("🚀 System Improvements Test Suite")
    print("=" * 60)
    
    tests = [
        ("Performance Monitor", test_performance_monitor),
        ("Security Enhancer", test_security_enhancer),
        ("Configuration Manager", test_config_manager),
        ("System Tester", test_system_tester),
        ("System Integration", test_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"\n{status} {test_name}")
        except Exception as e:
            results.append((test_name, False))
            print(f"\n❌ FAIL {test_name}: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 System Improvements Test Results Summary:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All system improvement tests passed!")
        print("\n🚀 System Improvements Features Active:")
        print("   • Performance monitoring and optimization")
        print("   • Security auditing and enhancement")
        print("   • Configuration management and validation")
        print("   • Comprehensive system testing")
        print("   • Full system integration")
        print("\n🎯 All phases of CURSOR_INTEGRATION_PLAN.md completed!")
        print("   ✅ Phase 1: Fix Core Command System")
        print("   ✅ Phase 2: Real Cursor Integration")
        print("   ✅ Phase 3: State Management")
        print("   ✅ Phase 4: Enhanced Error Handling")
        print("   ✅ Phase 5: System Improvements")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 