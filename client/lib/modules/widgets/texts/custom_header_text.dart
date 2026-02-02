import 'package:client/data/constants/constants.dart';
import 'package:client/modules/widgets/dividers/custom_vertical_divider.dart';
import 'package:flutter/material.dart';

class CustomHeaderText extends StatelessWidget {
  final String text;
  final double? fontSize;
  final Color? fontColor;
  const CustomHeaderText({
    required this.text,
    this.fontSize,
    this.fontColor,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        CustomVerticalDivider(
          color: AppColors.kSecondary,
          height: 20,
          width: 4,
        ),
        SizedBox(width: 5),
        Text(
          text,
          style: AppTypography.kBold24.copyWith(
            fontSize: fontSize ?? 24,
            color: fontColor,
          ),
        ),
      ],
    );
  }
}
