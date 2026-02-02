import 'package:client/data/constants/constants.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:flutter/material.dart';

import 'package:flutter_svg/svg.dart';

class RewardsMainCard extends StatelessWidget {
  const RewardsMainCard({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return PrimaryContainer(
      child: Column(
        children: [
          Container(
            height: 170,
            width: double.infinity,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: AppColors.kPrimary,
              borderRadius: BorderRadius.circular(20),
              image: DecorationImage(
                image: AssetImage(AppAssets.kRewards),
                fit: BoxFit.cover,
              ),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                SvgPicture.asset(
                  AppAssets.kBronzeBadge,
                  height: 45,
                  colorFilter: const ColorFilter.mode(
                    AppColors.kWhite,
                    BlendMode.srcIn,
                  ),
                ),
                Text(
                  '2,400',
                  style: AppTypography.kBold32.copyWith(
                    color: AppColors.kWhite,
                  ),
                ),
                Text(
                  'Current Points',
                  style: AppTypography.kLight12.copyWith(
                    color: AppColors.kWhite,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
