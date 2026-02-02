import 'dart:async';
import 'package:client/controllers/auth_controller.dart';
import 'package:client/data/constants/constants.dart';
import 'package:client/modules/auth/components/custom_otp_textfield.dart';
import 'package:client/modules/widgets/buttons/primary_button.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class VerificationCode extends StatefulWidget {
  const VerificationCode({super.key});

  @override
  State<VerificationCode> createState() => _VerificationCodeState();
}

class _VerificationCodeState extends State<VerificationCode> {
  final _verificationCodeController = TextEditingController();
  final AuthController _authController = Get.find<AuthController>();
  bool _formValidated = false;
  int _timerSeconds = 60;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    startTimer();
  }

  @override
  void dispose() {
    _timer?.cancel();
    _verificationCodeController.dispose();
    super.dispose();
  }

  void startTimer() {
    _timer = Timer.periodic(const Duration(seconds: 1), (Timer timer) {
      setState(() {
        if (_timerSeconds > 0) {
          _timerSeconds--;
        } else {
          timer.cancel();
        }
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    bool isDarkMode(BuildContext context) =>
        Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      backgroundColor:
          isDarkMode(context) ? AppColors.kDarkBackground : AppColors.kWhite,
      appBar: AppBar(
        leading: BackButton(
          onPressed: () {
            _authController.clearMessages();
            Navigator.pop(context);
          },
        ),
      ),
      body: Obx(() {
        if (_authController.verificationInProgress.value) {
          return Center(
            child: CircularProgressIndicator(color: AppColors.kPrimary),
          );
        }

        return SingleChildScrollView(
          padding: EdgeInsets.symmetric(horizontal: 20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(height: 80),
              Text('Verification Code', style: AppTypography.kBold32),
              Text(
                'We just send you a verification code. Check your\ninbox to get them.',
                style: AppTypography.kLight14,
              ),
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

              OTPField(
                onChanged: (value) {
                  if (value.isEmpty) {
                    setState(() {
                      _formValidated = false;
                    });
                  } else {
                    setState(() {
                      _formValidated = true;
                    });
                  }
                },
                controller: _verificationCodeController,
              ),
              SizedBox(height: 40),
              PrimaryButton(
                onTap:
                    _formValidated
                        ? () {
                          // Clear previous messages
                          _authController.clearMessages();

                          // Verify OTP
                          _authController
                              .verifyOTP(otp: _verificationCodeController.text)
                              .then((success) {
                                if (success) {
                                  // Navigate to landing page
                                  Get.offAllNamed('/landing');
                                }
                              });
                        }
                        : () {},
                text: 'Continue',
                color:
                    _formValidated
                        ? null
                        : isDarkMode(context)
                        ? AppColors.kDarkHint
                        : AppColors.kInput,
              ),
              SizedBox(height: 74),

              // Resend code
              if (_timerSeconds > 0)
                Center(
                  child: RichText(
                    text: TextSpan(
                      text: 'Resend Code in ',
                      style: AppTypography.kLight16.copyWith(
                        color:
                            isDarkMode(context)
                                ? AppColors.kWhite
                                : Colors.black,
                      ),
                      children: [
                        TextSpan(
                          text: '0:${_timerSeconds.toString().padLeft(2, '0')}',
                          style: AppTypography.kLight16.copyWith(
                            color: AppColors.kPrimary,
                          ),
                        ),
                      ],
                    ),
                  ),
                )
              else
                Center(
                  child: GestureDetector(
                    onTap: () {
                      setState(() {
                        _timerSeconds = 60;
                        _verificationCodeController.clear();
                        _formValidated = false;
                      });
                      _authController.resendOTP();
                      startTimer();
                    },
                    child: Text(
                      'Resend Code',
                      style: AppTypography.kMedium14.copyWith(
                        color: AppColors.kPrimary,
                        decoration: TextDecoration.underline,
                      ),
                    ),
                  ),
                ),
            ],
          ),
        );
      }),
    );
  }
}

// Export as Verification for backward compatibility
class Verification extends VerificationCode {
  const Verification({super.key});
}
