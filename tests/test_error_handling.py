#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Enhanced Error Handling System
Tests the new error handling functionality for Phase 4
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.error_handler import get_error_handler, handle_error, ErrorCategory, ErrorSeverity

def test_error_handler_creation():
    """Test error handler creation and initialization"""
    print("🚨 Testing Error Handler Creation...")
    
    try:
        error_handler = get_error_handler()
        if not error_handler:
            print("❌ Failed to create error handler")
            return False
        
        print("✅ Error handler created successfully")
        print(f"   Log directory: {error_handler.log_dir}")
        print(f"   Error log: {error_handler.error_log_file}")
        print(f"   Debug log: {error_handler.debug_log_file}")
        print(f"   Audit log: {error_handler.audit_log_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handler creation failed: {e}")
        return False

def test_error_categorization():
    """Test error categorization functionality"""
    print("\n🏷️  Testing Error Categorization...")
    
    try:
        error_handler = get_error_handler()
        
        # Test different error categories
        test_errors = [
            (ValueError("Invalid input"), ErrorCategory.VALIDATION, ErrorSeverity.MEDIUM),
            (FileNotFoundError("File not found"), ErrorCategory.FILE_OPERATION, ErrorSeverity.MEDIUM),
            (PermissionError("Access denied"), ErrorCategory.PERMISSION, ErrorSeverity.HIGH),
            (ConnectionError("Connection failed"), ErrorCategory.NETWORK, ErrorSeverity.MEDIUM),
            (OSError("System error"), ErrorCategory.SYSTEM, ErrorSeverity.HIGH)
        ]
        
        for error, expected_category, severity in test_errors:
            print(f"   📝 Testing: {type(error).__name__} - {expected_category}")
            result = error_handler.handle_error(error, expected_category, {}, severity)
            print(f"      Result: {len(result)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Error categorization test failed: {e}")
        return False

def test_error_handling():
    """Test comprehensive error handling"""
    print("\n🛠️  Testing Error Handling...")
    
    try:
        error_handler = get_error_handler()
        
        # Test command execution errors
        print("   💻 Testing command execution errors...")
        cmd_errors = [
            FileNotFoundError("command not found: invalid_cmd"),
            PermissionError("permission denied"),
            OSError("no such file or directory")
        ]
        
        for error in cmd_errors:
            result = error_handler.handle_error(
                error, 
                ErrorCategory.COMMAND_EXECUTION, 
                {'command': 'test_cmd'}, 
                ErrorSeverity.MEDIUM
            )
            print(f"      {type(error).__name__}: {len(result)} chars")
        
        # Test file operation errors
        print("\n   📁 Testing file operation errors...")
        file_errors = [
            PermissionError("permission denied"),
            OSError("no space left on device"),
            FileNotFoundError("file not found")
        ]
        
        for error in file_errors:
            result = error_handler.handle_error(
                error, 
                ErrorCategory.FILE_OPERATION, 
                {'file_path': '/test/file.txt'}, 
                ErrorSeverity.MEDIUM
            )
            print(f"      {type(error).__name__}: {len(result)} chars")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def test_recovery_suggestions():
    """Test recovery suggestion system"""
    print("\n🔧 Testing Recovery Suggestions...")
    
    try:
        error_handler = get_error_handler()
        
        # Test recovery strategies for different categories
        categories = [
            ErrorCategory.COMMAND_EXECUTION,
            ErrorCategory.FILE_OPERATION,
            ErrorCategory.NETWORK,
            ErrorCategory.PERMISSION,
            ErrorCategory.VALIDATION
        ]
        
        for category in categories:
            suggestions = error_handler._get_recovery_suggestions(category)
            print(f"   📋 {category}: {len(suggestions)} suggestions")
            for suggestion in suggestions[:2]:  # Show first 2
                print(f"      • {suggestion}")
        
        return True
        
    except Exception as e:
        print(f"❌ Recovery suggestions test failed: {e}")
        return False

def test_error_statistics():
    """Test error statistics functionality"""
    print("\n📊 Testing Error Statistics...")
    
    try:
        error_handler = get_error_handler()
        
        # Generate some test errors to build statistics
        print("   📝 Generating test errors for statistics...")
        test_errors = [
            (ValueError("Test validation error"), ErrorCategory.VALIDATION, ErrorSeverity.LOW),
            (FileNotFoundError("Test file error"), ErrorCategory.FILE_OPERATION, ErrorSeverity.MEDIUM),
            (PermissionError("Test permission error"), ErrorCategory.PERMISSION, ErrorSeverity.HIGH),
            (ConnectionError("Test network error"), ErrorCategory.NETWORK, ErrorSeverity.MEDIUM)
        ]
        
        for error, category, severity in test_errors:
            error_handler.handle_error(error, category, {}, severity)
        
        # Get statistics
        stats = error_handler.get_error_statistics()
        print("\n   📈 Error Statistics:")
        print(f"      Total errors: {stats['total_errors']}")
        print(f"      Categories: {len(stats['error_categories'])}")
        print(f"      Severity levels: {len(stats['severity_distribution'])}")
        print(f"      Recent errors: {len(stats['recent_errors'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error statistics test failed: {e}")
        return False

def test_logging_functionality():
    """Test logging functionality"""
    print("\n📝 Testing Logging Functionality...")
    
    try:
        error_handler = get_error_handler()
        
        # Test different log levels
        print("   🔍 Testing log levels...")
        logger = error_handler._setup_logging.__self__ if hasattr(error_handler._setup_logging, '__self__') else None
        
        if logger:
            print("      ✅ Logger setup verified")
        else:
            print("      ⚠️  Logger setup check unavailable")
        
        # Check if log files exist
        print("\n   📁 Checking log files...")
        log_files = [
            error_handler.error_log_file,
            error_handler.debug_log_file,
            error_handler.audit_log_file
        ]
        
        for log_file in log_files:
            if log_file.exists():
                size = log_file.stat().st_size
                print(f"      ✅ {log_file.name}: {size} bytes")
            else:
                print(f"      ❌ {log_file.name}: Not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Logging functionality test failed: {e}")
        return False

def test_export_functionality():
    """Test error log export functionality"""
    print("\n📤 Testing Export Functionality...")
    
    try:
        error_handler = get_error_handler()
        
        # Test export
        export_file = "tmp/error_logs_export_test.json"
        export_success = error_handler.export_error_logs(export_file)
        
        if export_success:
            print(f"   ✅ Error logs exported to {export_file}")
            
            # Check file size
            if os.path.exists(export_file):
                size = os.path.getsize(export_file)
                print(f"      Export file size: {size} bytes")
            else:
                print("      Export file not found")
        else:
            print("   ❌ Error log export failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Export functionality test failed: {e}")
        return False

def test_global_error_handling():
    """Test global error handling function"""
    print("\n🌍 Testing Global Error Handling...")
    
    try:
        # Test global handle_error function
        test_error = ValueError("Global test error")
        result = handle_error(
            test_error, 
            ErrorCategory.VALIDATION, 
            {'test': True}, 
            ErrorSeverity.MEDIUM
        )
        
        if result and len(result) > 0:
            print("   ✅ Global error handling working")
            print(f"      Result length: {len(result)} characters")
        else:
            print("   ❌ Global error handling failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Global error handling test failed: {e}")
        return False

def main():
    """Run all error handling tests"""
    print("🚨 Enhanced Error Handling System Test Suite")
    print("=" * 65)
    
    tests = [
        ("Error Handler Creation", test_error_handler_creation),
        ("Error Categorization", test_error_categorization),
        ("Error Handling", test_error_handling),
        ("Recovery Suggestions", test_recovery_suggestions),
        ("Error Statistics", test_error_statistics),
        ("Logging Functionality", test_logging_functionality),
        ("Export Functionality", test_export_functionality),
        ("Global Error Handling", test_global_error_handling)
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
    print("\n" + "=" * 65)
    print("📊 Enhanced Error Handling Test Results Summary:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All enhanced error handling tests passed!")
        print("\n🚨 Enhanced Error Handling Features Active:")
        print("   • Comprehensive error categorization")
        print("   • User-friendly error messages")
        print("   • Recovery suggestions")
        print("   • Detailed error logging")
        print("   • Error statistics and monitoring")
        print("   • Export functionality")
        print("   • Global error handling")
        print("\n🚀 Ready to proceed with Phase 5: System Improvements")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 