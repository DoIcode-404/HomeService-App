class LocalStorageKeys {
  // Theme
  static const String theme = 'theme';

  // Authentication
  static const String authToken = 'auth_token';
  static const String refreshToken = 'refresh_token';
  static const String userId = 'user_id';
  static const String userPhone = 'user_phone';
  static const String userEmail = 'user_email';
  static const String userName = 'user_name';
  static const String userProfilePic = 'user_profile_pic';
  static const String isLoggedIn = 'is_logged_in';

  // User data
  static const String userData = 'user_data';
  static const String userRole = 'user_role';

  // App preferences
  static const String firstLaunch = 'first_launch';
  static const String language = 'language';
  static const String notificationsEnabled = 'notifications_enabled';

  // Cache
  static const String cachedCategories = 'cached_categories';
  static const String cachedServices = 'cached_services';
}

/// Theme Options
class ThemeOptions {
  static const String light = 'light';
  static const String dark = 'dark';
  static const String system = 'system';
}
