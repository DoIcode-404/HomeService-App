import 'package:client/model/category_model.dart';
import 'package:client/modules/categories/sub_category_view.dart';
import 'package:client/modules/widgets/animations/button_animation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:get/get.dart';
import '../../../data/constants/constants.dart';

class CategoryCard extends StatelessWidget {
  final CategoryModel category;
  final bool isGridView;
  const CategoryCard({
    required this.category,
    this.isGridView = false,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return ButtonAnimation(
      onTap: () {
        Get.to(() => SubCategoryView(category: category));
      },
      child: Column(
        children: [
          Container(
            height: isGridView ? 72 : 58,
            width: isGridView ? 72 : 58,
            alignment: Alignment.center,
            padding: EdgeInsets.all(18),
            decoration: BoxDecoration(
              color: category.color,
              shape: BoxShape.circle,
            ),
            child: SvgPicture.asset(category.image),
          ),
          SizedBox(height: 12),
          Text(category.name, style: AppTypography.kLight13),
        ],
      ),
    );
  }
}

class CategorySeeAllButton extends StatelessWidget {
  final VoidCallback onTap;
  const CategorySeeAllButton({required this.onTap, super.key});

  @override
  Widget build(BuildContext context) {
    bool isDarkMode(BuildContext context) =>
        Theme.of(context).brightness == Brightness.dark;

    return ButtonAnimation(
      onTap: onTap,
      child: Column(
        children: [
          Container(
            height: 58,
            width: 58,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color:
                  isDarkMode(context)
                      ? AppColors.kContentColor
                      : const Color(0xFFECECEC),
              shape: BoxShape.circle,
            ),
            child: const Icon(Icons.arrow_forward),
          ),
          SizedBox(height: 12),
          Text('See All', style: AppTypography.kLight13),
        ],
      ),
    );
  }
}
