import 'package:client/data/constants/constants.dart';
import 'package:flutter/material.dart';

class PhoneNumberCard extends StatelessWidget {
  const PhoneNumberCard({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        CircleAvatar(
          radius: 30,
          backgroundImage: AssetImage(AppAssets.kProfilePic),
        ),
        SizedBox(width: 16),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('+64 012 3456', style: AppTypography.kBold16),
            SizedBox(height: 5),
            Text(
              'Primary',
              style: AppTypography.kLight13.copyWith(color: AppColors.kHint),
            ),
          ],
        ),
      ],
    );
  }
}
