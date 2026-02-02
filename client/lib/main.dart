import 'package:client/bindings/auth_binding.dart';
import 'package:client/controllers/theme_controller.dart';
import 'package:client/data/constants/app_theme.dart';
import 'package:client/routes/app_routes.dart';
import 'package:client/services/theme_services.dart';
import 'package:device_preview/device_preview.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize GetStorage
  await GetStorage.init();

  SystemChrome.setSystemUIOverlayStyle(defaultOverlay);
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);

  runApp(
    kIsWeb
        ? DevicePreview(enabled: true, builder: (context) => const MyApp())
        : const MyApp(),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    final themeController = Get.put(ThemeController());

    return GetMaterialApp(
      useInheritedMediaQuery: true,
      locale: DevicePreview.locale(context),
      builder: DevicePreview.appBuilder,
      title: 'Door Service',
      debugShowCheckedModeBanner: false,

      // Initialize Auth binding
      initialBinding: AuthBinding(),

      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: getThemeMode(themeController.theme),
      initialRoute: AppRoutes.getOnboardingRoute(),
      getPages: AppRoutes.routes,
    );
  }
}
