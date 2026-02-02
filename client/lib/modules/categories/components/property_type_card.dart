import 'package:client/data/constants/constants.dart';
import 'package:client/model/property_type.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

class PropertyTypeCard extends StatelessWidget {
  final PropertyType property;
  final VoidCallback onTap;
  final bool isSelected;
  const PropertyTypeCard({
    super.key,
    required this.property,
    required this.onTap,
    required this.isSelected,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Column(
        children: [
          Container(
            height: 65,
            width: 65,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(10),
              color: isSelected ? AppColors.kPrimary : null,
              border: isSelected ? null : Border.all(color: AppColors.kHint),
            ),
            child: SvgPicture.asset(
              property.image,
              colorFilter: ColorFilter.mode(
                isSelected ? AppColors.kWhite : AppColors.kHint,
                BlendMode.srcIn,
              ),
            ),
          ),
          SizedBox(height: 10),
          Text(property.name, style: AppTypography.kLight13),
        ],
      ),
    );
  }
}
