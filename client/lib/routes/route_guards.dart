import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:client/controllers/auth_controller.dart';

/// Route Guard - Middleware for protected routes
class AuthGuard extends GetMiddleware {
  @override
  RouteSettings? redirect(String? route) {
    final authController = Get.find<AuthController>();
    if (!authController.isLoggedIn.value) {
      return RouteSettings(name: '/auth');
    }
    return null;
  }
}

/// Route Guard - Redirect logged-in users away from auth pages
class PublicGuard extends GetMiddleware {
  @override
  RouteSettings? redirect(String? route) {
    final authController = Get.find<AuthController>();
    if (authController.isLoggedIn.value) {
      return RouteSettings(name: '/home');
    }
    return null;
  }
}
