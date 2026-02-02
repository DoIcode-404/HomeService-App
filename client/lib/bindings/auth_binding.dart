import 'package:get/get.dart';
import 'package:client/controllers/auth_controller.dart';

class AuthBinding extends Bindings {
  @override
  void dependencies() {
    // Create and put Auth Controller
    Get.put<AuthController>(
      AuthController(),
      permanent: true, // Keep in memory throughout app lifecycle
    );
  }
}
