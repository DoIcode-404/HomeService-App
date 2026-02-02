import 'package:client/modules/onboarding/onboarding_screen.dart';
import 'package:client/modules/auth/sign_in.dart';
import 'package:client/modules/auth/sign_up.dart';
import 'package:client/modules/auth/verification.dart';
import 'package:client/modules/landing/landing_page.dart';
import 'package:client/modules/home/home_view.dart';
import 'package:client/routes/route_guards.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class AppRoutes {
  // Public Routes
  static const String onboarding = '/';
  static const String signIn = '/auth/signin';
  static const String signUp = '/auth/signup';
  static const String verification = '/auth/verification';

  // Protected Routes
  static const String landing = '/landing';
  static const String home = '/home';

  static List<GetPage> routes = [
    // Onboarding
    GetPage(
      name: onboarding,
      page: () => const OnboardingScreen(),
      middlewares: [PublicGuard()],
    ),

    // Authentication Routes
    GetPage(
      name: signIn,
      page: () => const SignIn(),
      middlewares: [PublicGuard()],
    ),
    GetPage(
      name: signUp,
      page: () => const SignUp(),
      middlewares: [PublicGuard()],
    ),
    GetPage(
      name: verification,
      page: () => const Verification(),
      middlewares: [PublicGuard()],
    ),

    // Protected Routes
    GetPage(
      name: landing,
      page: () => const LandingPage(),
      middlewares: [AuthGuard()],
    ),
    GetPage(
      name: home,
      page: () => HomeView(drawerKey: GlobalKey<ScaffoldState>()),
      middlewares: [AuthGuard()],
    ),
  ];

  static String getOnboardingRoute() => onboarding;
  static String getSignInRoute() => signIn;
  static String getSignUpRoute() => signUp;
  static String getVerificationRoute() => verification;
  static String getHomeRoute() => home;
  static String getLandingRoute() => landing;
}
