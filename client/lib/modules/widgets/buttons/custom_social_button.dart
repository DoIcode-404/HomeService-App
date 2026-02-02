import 'package:client/data/constants/constants.dart';
import 'package:client/modules/widgets/animations/button_animation.dart';
import 'package:flutter/material.dart';

import 'package:flutter_svg/flutter_svg.dart';

class CustomSocialButton extends StatelessWidget {
  final VoidCallback onTap;
  final String icon;
  const CustomSocialButton({
    super.key,
    required this.onTap,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    bool isDarkMode(BuildContext context) =>
        Theme.of(context).brightness == Brightness.dark;

    return ButtonAnimation(
      onTap: onTap,
      child: Container(
        height: 55,
        width: 55,
        alignment: Alignment.center,
        padding: EdgeInsets.all(1),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(AppSpacing.radiusTen),
          color:
              isDarkMode(context) ? AppColors.kDarkHint : AppColors.kNeutral01,
          border: Border.all(
            color:
                isDarkMode(context)
                    ? AppColors.kDarkInput
                    : AppColors.kNeutral03,
            width: 2,
          ),
        ),
        child: SvgPicture.asset(icon),
      ),
    );
  }
}
