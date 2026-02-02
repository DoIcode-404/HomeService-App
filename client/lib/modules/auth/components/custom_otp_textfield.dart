import 'package:client/data/constants/constants.dart';
import 'package:flutter/material.dart';

class OTPField extends StatefulWidget {
  final Function(String) onChanged;
  final TextEditingController controller;
  const OTPField({
    super.key,
    required this.onChanged,
    required this.controller,
  });

  @override
  _OTPFieldState createState() => _OTPFieldState();
}

class _OTPFieldState extends State<OTPField> {
  List<FocusNode> focusNodes = [];
  List<TextEditingController> controllers = [];

  @override
  void initState() {
    super.initState();
    for (int i = 0; i < 4; i++) {
      focusNodes.add(FocusNode());
      controllers.add(TextEditingController());
    }
  }

  @override
  void dispose() {
    for (var controller in controllers) {
      controller.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    bool isDarkMode(BuildContext context) =>
        Theme.of(context).brightness == Brightness.dark;

    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: List.generate(
        4,
        (index) => Container(
          width: 55,
          height: 64,
          decoration: BoxDecoration(
            color:
                isDarkMode(context) ? AppColors.kDarkInput : AppColors.kInput,
            borderRadius: BorderRadius.circular(5),
          ),
          child: TextField(
            controller: controllers[index],
            focusNode: focusNodes[index],
            textAlignVertical: TextAlignVertical.center,
            onChanged: (value) {
              // Update the parent controller with the complete OTP
              String otp = getOTP();
              widget.controller.text = otp;
              widget.onChanged(otp);

              if (value.isNotEmpty) {
                if (index < 3) {
                  focusNodes[index + 1].requestFocus();
                }
              } else if (value.isEmpty && index > 0) {
                focusNodes[index - 1].requestFocus();
              }
            },
            keyboardType: TextInputType.number,
            textAlign: TextAlign.center,
            maxLength: 1,
            style: AppTypography.kMedium18,
            decoration: InputDecoration(
              hintText: '•',
              counterText: '',
              contentPadding: EdgeInsets.only(top: 50, left: 3),
            ),
          ),
        ),
      ),
    );
  }

  String getOTP() {
    String otp = '';
    for (var controller in controllers) {
      otp += controller.text;
    }
    return otp;
  }
}
