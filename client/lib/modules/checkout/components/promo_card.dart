import 'package:client/data/constants/constants.dart';
import 'package:flutter/material.dart';

import 'package:flutter_svg/flutter_svg.dart';

class PromoCard extends StatelessWidget {
  final VoidCallback? onTap;
  final bool isSelected;
  const PromoCard({super.key, this.onTap, this.isSelected = false});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Row(
        children: [
          Container(
            height: 55,
            width: 55,
            alignment: Alignment.center,
            decoration: const BoxDecoration(
              shape: BoxShape.circle,
              color: AppColors.kLime,
            ),
            child: SvgPicture.asset(AppAssets.kPromoCode),
          ),
          SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Service HUB 21', style: AppTypography.kMedium16),
                SizedBox(height: 5),
                Text(
                  'You will get 20% discount for this promo code.',
                  style: AppTypography.kLight13.copyWith(
                    color: AppColors.kNeutral,
                  ),
                ),
              ],
            ),
          ),
          Container(
            height: 20,
            width: 20,
            padding: EdgeInsets.all(2),
            decoration: BoxDecoration(
              border: Border.all(color: AppColors.kPrimary, width: 2),
              shape: BoxShape.circle,
            ),
            child:
                isSelected
                    ? Container(
                      decoration: const BoxDecoration(
                        color: AppColors.kPrimary,
                        shape: BoxShape.circle,
                      ),
                    )
                    : null,
          ),
        ],
      ),
    );
  }
}
