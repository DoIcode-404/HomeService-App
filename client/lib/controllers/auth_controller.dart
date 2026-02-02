import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';
import 'package:client/model/user_model.dart';

class AuthController extends GetxController {
  // Observables
  final isLoading = false.obs;
  final isLoggedIn = false.obs;
  final currentUser = Rx<UserModel?>(null);
  final authToken = RxString('');
  final errorMessage = RxString('');
  final successMessage = RxString('');

  // Storage
  final GetStorage _storage = GetStorage();

  // States
  final otpSent = false.obs;
  final verificationInProgress = false.obs;
  final tempPhone = RxString('');

  @override
  void onInit() {
    super.onInit();
    _checkAutoLogin();
  }

  /// Check if user was previously logged in and auto-login
  Future<void> _checkAutoLogin() async {
    try {
      final token = _storage.read('auth_token');
      final isLoggedInStored = _storage.read('is_logged_in') ?? false;

      if (token != null && isLoggedInStored) {
        authToken.value = token;
        isLoggedIn.value = true;

        // Load user data from storage
        final userId = _storage.read('user_id');
        final userName = _storage.read('user_name');
        final userProfilePic = _storage.read('user_profile_pic');

        if (userId != null) {
          currentUser.value = UserModel(
            id: userId,
            name: userName ?? '',
            profilePic: userProfilePic ?? '',
          );
        }
      }
    } catch (e) {
      print('Auto-login check failed: $e');
    }
  }

  /// Login with phone number - sends OTP (Mock for frontend-only)
  Future<void> login({required String phone}) async {
    try {
      clearMessages();
      isLoading.value = true;

      print('Login attempt with phone: $phone');

      // Simulate OTP sending (frontend-only mock)
      await Future.delayed(Duration(seconds: 1));

      otpSent.value = true;
      tempPhone.value = phone;
      successMessage.value = 'OTP sent successfully';
      print('OTP sent successfully for phone: $phone');
    } catch (e) {
      errorMessage.value = 'An unexpected error occurred. Please try again.';
      print('Login error: $e');
    } finally {
      isLoading.value = false;
    }
  }

  /// Verify OTP and complete login (Mock for frontend-only)
  Future<bool> verifyOTP({required String otp}) async {
    try {
      clearMessages();
      verificationInProgress.value = true;
      isLoading.value = true;

      // Simulate OTP verification (frontend-only mock)
      await Future.delayed(Duration(seconds: 1));

      // Mock success for demo (accept any 4-digit OTP)
      if (otp.length == 4) {
        final mockToken = 'mock_token_${DateTime.now().millisecondsSinceEpoch}';
        final mockUserId = 'user_${tempPhone.value}';

        await _storage.write('auth_token', mockToken);
        await _storage.write('is_logged_in', true);
        await _storage.write('user_id', mockUserId);
        await _storage.write('user_phone', tempPhone.value);
        await _storage.write('user_name', 'User ${tempPhone.value}');

        authToken.value = mockToken;
        isLoggedIn.value = true;
        successMessage.value = 'Logged in successfully';

        currentUser.value = UserModel(
          id: mockUserId,
          name: 'User ${tempPhone.value}',
          profilePic: '',
        );

        otpSent.value = false;
        tempPhone.value = '';
        return true;
      } else {
        errorMessage.value = 'Invalid OTP. Please try again.';
        return false;
      }
    } catch (e) {
      errorMessage.value = 'Verification failed. Please try again.';
      print('OTP verification error: $e');
      return false;
    } finally {
      verificationInProgress.value = false;
      isLoading.value = false;
    }
  }

  /// Sign up with user details (Mock for frontend-only)
  Future<bool> signup({
    required String phone,
    required String email,
    required String name,
    String? otp,
  }) async {
    try {
      clearMessages();
      isLoading.value = true;

      // Simulate signup (frontend-only mock)
      await Future.delayed(Duration(seconds: 1));

      final mockToken = 'mock_token_${DateTime.now().millisecondsSinceEpoch}';
      final mockUserId = 'user_$phone';

      await _storage.write('auth_token', mockToken);
      await _storage.write('is_logged_in', true);
      await _storage.write('user_id', mockUserId);
      await _storage.write('user_phone', phone);
      await _storage.write('user_email', email);
      await _storage.write('user_name', name);

      authToken.value = mockToken;
      isLoggedIn.value = true;
      successMessage.value = 'Account created successfully';

      currentUser.value = UserModel(id: mockUserId, name: name, profilePic: '');

      return true;
    } catch (e) {
      errorMessage.value = 'Sign up failed. Please try again.';
      print('Signup error: $e');
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  /// Logout user
  Future<void> logout() async {
    try {
      isLoading.value = true;

      await _storage.remove('auth_token');
      await _storage.remove('is_logged_in');
      await _storage.remove('user_id');
      await _storage.remove('user_phone');
      await _storage.remove('user_email');
      await _storage.remove('user_name');
      await _storage.remove('user_profile_pic');

      isLoggedIn.value = false;
      authToken.value = '';
      currentUser.value = null;
      otpSent.value = false;
      tempPhone.value = '';

      clearMessages();
    } catch (e) {
      errorMessage.value = 'Logout failed';
      print('Logout error: $e');
    } finally {
      isLoading.value = false;
    }
  }

  /// Resend OTP (Mock for frontend-only)
  Future<void> resendOTP() async {
    try {
      clearMessages();
      isLoading.value = true;

      if (tempPhone.value.isEmpty) {
        errorMessage.value = 'Phone number not found. Please login again.';
        return;
      }

      await login(phone: tempPhone.value);
      successMessage.value = 'OTP resent successfully';
    } catch (e) {
      errorMessage.value = 'Failed to resend OTP. Please try again.';
      print('Resend OTP error: $e');
    } finally {
      isLoading.value = false;
    }
  }

  /// Refresh auth token (Mock for frontend-only)
  Future<void> refreshAuthToken() async {
    try {
      // Mock token refresh - just keep current state
      print('Token refresh called (mock)');
    } catch (e) {
      print('Token refresh error: $e');
    }
  }

  /// Get auth header for API requests
  String getAuthHeader() {
    return 'Bearer ${authToken.value}';
  }

  /// Clear error and success messages
  void clearMessages() {
    errorMessage.value = '';
    successMessage.value = '';
  }

  /// Get user initials for avatar
  String getUserInitials() {
    if (currentUser.value?.name.isNotEmpty == true) {
      final names = currentUser.value!.name.split(' ');
      if (names.length > 1) {
        return '${names[0][0]}${names[1][0]}'.toUpperCase();
      }
      return names[0][0].toUpperCase();
    }
    return 'U';
  }
}
