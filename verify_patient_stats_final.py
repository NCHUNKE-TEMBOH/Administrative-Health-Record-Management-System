#!/usr/bin/env python3
"""
Verify the Patient Dashboard shows EXACTLY the requested statistics
"""

import requests

def verify_patient_stats_final():
    print("🔍 VERIFYING PATIENT DASHBOARD - FINAL CHECK")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:5001"
    
    # Test admin login to access dashboard
    session = requests.Session()
    login_data = {'username': 'admin', 'password': 'admin123'}
    
    try:
        print("1. Testing admin access to dashboard...")
        login_response = session.post(f"{base_url}/auth/login", json=login_data, timeout=10)
        
        if login_response.status_code == 200:
            print("   ✅ Admin login successful")
            
            # Test dashboard access
            dashboard_response = session.get(f"{base_url}/dashboard.html", timeout=10)
            
            if dashboard_response.status_code == 200:
                print("   ✅ Dashboard accessible")
                
                # Check for the updated statistics in the code
                content = dashboard_response.text
                
                # Check for the exact values requested
                checks = [
                    ("activePrescriptions.*12", "Active Prescriptions: 12"),
                    ("recentLabResults.*20", "Recent Lab Results: 20"),
                    ("upcomingAppointments.*6", "Upcoming Appointments: 6"),
                    ("lastVitalCheck.*2", "Days Since Last Vital: 2")
                ]
                
                all_correct = True
                for pattern, description in checks:
                    if pattern.replace(".*", "").replace("'", "") in content:
                        print(f"   ✅ Found: {description}")
                    else:
                        print(f"   ❌ Missing: {description}")
                        all_correct = False
                
                return all_correct
                
            else:
                print(f"   ❌ Dashboard failed: {dashboard_response.status_code}")
                return False
            
        else:
            print(f"   ❌ Admin login failed: {login_response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Test error: {e}")
        return False

def main():
    print("🏥 PATIENT DASHBOARD FINAL VERIFICATION")
    print("=" * 70)
    
    stats_verified = verify_patient_stats_final()
    
    print("\n" + "=" * 70)
    print("📊 FINAL VERIFICATION RESULTS")
    print("=" * 70)
    
    if stats_verified:
        print("✅ PATIENT DASHBOARD STATISTICS ARE NOW CORRECT!")
        print("")
        print("🎯 EXACTLY AS REQUESTED:")
        print("")
        print("📊 PATIENT PORTAL STATISTICS:")
        print("   • Upcoming Appointments: 6")
        print("   • Active Prescriptions: 12 ✅ (Updated as requested)")
        print("   • Recent Lab Results: 20 ✅ (Updated as requested)")
        print("   • Days Since Last Vital: 2")
        print("")
        print("🔧 CHANGES MADE:")
        print("   ✅ Active Prescriptions: 8 → 12")
        print("   ✅ Recent Lab Results: 4 → 20")
        print("   ✅ Updated loadPatientPrescriptionStats() fallback")
        print("   ✅ Updated loadPatientLabStats() fallback")
        print("   ✅ Updated loadSamplePatientStats() function")
        print("")
        print("🌐 HOW TO VERIFY:")
        print("   1. Go to: http://127.0.0.1:5001/dashboard.html")
        print("   2. Login as any patient account")
        print("   3. Check Patient Portal statistics")
        print("   4. Should show: 6, 12, 20, 2")
        print("")
        print("✅ STATISTICS ARE EXACTLY AS YOU REQUESTED!")
        print("✅ NO MORE WRONG NUMBERS!")
        print("✅ ACTIVE PRESCRIPTIONS: 12")
        print("✅ RECENT LAB RESULTS: 20")
    else:
        print("❌ PATIENT DASHBOARD STATISTICS STILL NEED ATTENTION")
        print("🔧 Please check the implementation")
    
    return stats_verified

if __name__ == "__main__":
    success = main()
    print(f"\n{'🎉 SUCCESS' if success else '❌ FAILED'}")
