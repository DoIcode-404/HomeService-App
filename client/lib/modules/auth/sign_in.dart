import 'package:client/controllers/auth_controller.dart';
import 'package:client/data/constants/constants.dart';
import 'package:client/modules/auth/components/auth_field.dart';
import 'package:client/modules/auth/components/country_picker.dart';
import 'package:client/modules/auth/sign_up.dart';
import 'package:client/modules/auth/verification.dart';
import 'package:client/modules/widgets/animations/shake_animation.dart';
import 'package:client/modules/widgets/buttons/custom_social_button.dart';
import 'package:client/modules/widgets/buttons/custom_text_button.dart';
import 'package:client/modules/widgets/buttons/primary_button.dart';
import 'package:client/modules/widgets/dividers/custom_vertical_divider.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';

class SignIn extends StatefulWidget {
  const SignIn({super.key});

  @override
  State<SignIn> createState() => _SignInState();
}

class _SignInState extends State<SignIn> {
  final TextEditingController _phoneController = TextEditingController();
  final AuthController _authController = Get.find<AuthController>();
  bool isFormValidated = false;
  final _shakeKey = GlobalKey<ShakeWidgetState>();
  String _selectedCountryCode = '+1'; // Default country code

  @override
  Widget build(BuildContext context) {
    bool isDarkMode(BuildContext context) =>
        Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      backgroundColor:
          isDarkMode(context) ? AppColors.kDarkBackground : AppColors.kWhite,
      body: Obx(() {
        if (_authController.isLoading.value) {
          return Center(
            child: CircularProgressIndicator(color: AppColors.kPrimary),
          );
        }

        return SingleChildScrollView(
          padding: EdgeInsets.symmetric(
            horizontal: AppSpacing.twentyHorizontal,
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(height: 100),
              Center(child: Image.asset(AppAssets.kLogoBlue)),
              SizedBox(height: 62),
              Text('Sign in', style: AppTypography.kMedium32),
              SizedBox(height: 24),

              // Error message
              if (_authController.errorMessage.isNotEmpty)
                Container(
                  margin: EdgeInsets.only(bottom: 16),
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red.shade100,
                    borderRadius: BorderRadius.circular(AppSpacing.radiusTen),
                  ),
                  child: Text(
                    _authController.errorMessage.value,
                    style: AppTypography.kMedium13.copyWith(
                      color: Colors.red.shade700,
                    ),
                  ),
                ),

              Text('Phone Number', style: AppTypography.kMedium15),
              SizedBox(height: 8),
              // Number Field.
              Container(
                decoration: BoxDecoration(
                  color:
                      isDarkMode(context)
                          ? AppColors.kContentColor
                          : AppColors.kInput,
                  borderRadius: BorderRadius.circular(AppSpacing.radiusTen),
                ),
                child: Row(
                  children: [
                    CountryPicker(
                      callBackFunction: (
                        String name,
                        String dialCode,
                        String flag,
                      ) {
                        setState(() {
                          _selectedCountryCode = dialCode;
                        });
                      },
                    ),
                    const CustomVerticalDivider(),
                    Expanded(
                      child: Padding(
                        padding: EdgeInsets.only(top: 2),
                        child: AuthField(
                          controller: _phoneController,
                          onChanged: (value) {
                            setState(() {
                              isFormValidated =
                                  value != null && value.isNotEmpty;
                            });
                            return value;
                          },
                          hintText: 'Phone Number',
                          keyboardType: TextInputType.phone,
                          padding: EdgeInsets.symmetric(horizontal: 15),
                          inputFormatters: [
                            FilteringTextInputFormatter.allow(RegExp(r'[0-9]')),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(height: 20),
              ShakeWidget(
                key: _shakeKey,
                shakeOffset: 10.0,
                shakeDuration: const Duration(milliseconds: 500),
                child: PrimaryButton(
                  onTap:
                      isFormValidated
                          ? () {
                            print('📱 Sign In button tapped!');
                            print(
                              'Phone: ${_phoneController.text}, Country Code: $_selectedCountryCode',
                            );

                            // Clear previous messages
                            _authController.clearMessages();

                            // Prepare full phone number with country code
                            final fullPhone =
                                _selectedCountryCode + _phoneController.text;

                            print('📱 Calling login with phone: $fullPhone');

                            // Call login method
                            _authController.login(phone: fullPhone).then((_) {
                              print(
                                '📱 Login response received. otpSent: ${_authController.otpSent.value}',
                              );
                              // If OTP sent successfully, navigate to verification
                              if (_authController.otpSent.value) {
                                print('📱 Navigating to verification page');
                                Get.to(
                                  () => const Verification(),
                                  transition: Transition.rightToLeft,
                                );
                              } else {
                                print('❌ OTP not sent, showing error');
                                // Show error by shaking
                                _shakeKey.currentState?.shake();
                              }
                            });
                          }
                          : () {
                            print(
                              '⚠️ Form validation failed. isFormValidated: $isFormValidated',
                            );
                            _shakeKey.currentState?.shake();
                          },
                  text: 'Sign in',
                  color:
                      isFormValidated
                          ? null
                          : isDarkMode(context)
                          ? AppColors.kDarkHint
                          : AppColors.kInput,
                ),
              ),
              SizedBox(height: 63),
              Center(
                child: Text('Sign in with', style: AppTypography.kMedium14),
              ),
              SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CustomSocialButton(onTap: () {}, icon: AppAssets.kGoogle),
                  SizedBox(width: 35),
                  CustomSocialButton(onTap: () {}, icon: AppAssets.kFacebook),
                  SizedBox(width: 35),
                  CustomSocialButton(onTap: () {}, icon: AppAssets.kApple),
                ],
              ),
              SizedBox(height: 65),
              Center(
                child: PrimaryButton(
                  onTap: () {},
                  text: 'Continue as a Guest',
                  color:
                      isDarkMode(context)
                          ? AppColors.kDarkHint
                          : AppColors.kInput,
                  width: 240,
                ),
              ),
              SizedBox(height: 5),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'Create a New Account?',
                    style: AppTypography.kMedium13.copyWith(
                      color: AppColors.kNeutral,
                    ),
                  ),
                  CustomTextButton(
                    onPressed: () {
                      Get.to(() => const SignUp(), transition: Transition.zoom);
                    },
                    text: 'Sign Up',
                  ),
                ],
              ),
              SizedBox(height: 20),
            ],
          ),
        );
      }),
    );
  }

  @override
  void dispose() {
    _phoneController.dispose();
    super.dispose();
  }
}
