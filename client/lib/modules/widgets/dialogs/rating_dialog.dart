import 'package:client/data/constants/constants.dart';
import 'package:client/modules/widgets/buttons/primary_button.dart';
import 'package:client/modules/widgets/dialogs/components/rating_field.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class RatingDialog extends StatelessWidget {
  final Animation<double> opacity;
  final Animation<double> scale;
  const RatingDialog({super.key, required this.opacity, required this.scale});

  @override
  Widget build(BuildContext context) {
    bool isDarkMode(BuildContext context) =>
        Theme.of(context).brightness == Brightness.dark;

    return Transform.scale(
      scale: scale.value,
      child: Opacity(
        opacity: opacity.value,
        child: AlertDialog(
          insetPadding: EdgeInsets.symmetric(horizontal: 10),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
          ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Image.asset(AppAssets.kLogo),
              SizedBox(height: 16),
              Text('Rate Door-Hub App', style: AppTypography.kBold20),
              SizedBox(height: 10),
              Text(
                'Your feedback will help us to make improvements',
                style: AppTypography.kLight14,
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 16),
              CustomRatingField(onChanged: (value) {}),
              SizedBox(height: 20),
              Row(
                children: [
                  Expanded(
                    flex: 4,
                    child: PrimaryButton(
                      onTap: () {
                        Get.back();
                      },
                      text: 'No, Thanks',
                      width: 60,
                      color:
                          isDarkMode(context)
                              ? AppColors.kContentColor
                              : AppColors.kWhite,
                      isBorder: true,
                    ),
                  ),
                  SizedBox(width: 10),
                  Expanded(
                    flex: 6,
                    child: PrimaryButton(
                      onTap: () {
                        Get.back();
                      },
                      text: 'Rate on Play Store',
                      width: 60,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
