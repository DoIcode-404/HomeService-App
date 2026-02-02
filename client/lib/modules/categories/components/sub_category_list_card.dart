import 'package:animations/animations.dart';
import 'package:client/data/constants/constants.dart';
import 'package:client/model/service_model.dart';
import 'package:client/modules/categories/components/rating_widget.dart';
import 'package:client/modules/categories/services_detail_view.dart';

import 'package:flutter/material.dart';

class SubCategoryListCard extends StatelessWidget {
  final ServicesModel service;
  const SubCategoryListCard({super.key, required this.service});

  @override
  Widget build(BuildContext context) {
    bool isDarkMode(BuildContext context) =>
        Theme.of(context).brightness == Brightness.dark;

    return OpenContainer(
      transitionType: ContainerTransitionType.fadeThrough,
      openBuilder: (BuildContext _, VoidCallback openContainer) {
        return ServicesDetailView(services: service);
      },
      middleColor:
          isDarkMode(context) ? AppColors.kDarkSurfaceColor : AppColors.kWhite,
      openColor:
          isDarkMode(context) ? AppColors.kDarkSurfaceColor : AppColors.kWhite,
      closedColor:
          isDarkMode(context) ? AppColors.kDarkSurfaceColor : AppColors.kWhite,

      closedShape: const RoundedRectangleBorder(),
      closedElevation: 0.0,
      closedBuilder: (BuildContext _, VoidCallback openContainer) {
        return InkWell(
          onTap: openContainer,
          child: Row(
            children: [
              Container(
                height: 116,
                width: 105,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(10),
                  image: DecorationImage(
                    image: AssetImage(service.image),
                    fit: BoxFit.cover,
                  ),
                ),
              ),
              SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        RatingWidget(service: service),
                        const Spacer(),
                        const Icon(Icons.more_horiz),
                      ],
                    ),
                    SizedBox(height: 5),
                    Text(service.name, style: AppTypography.kMedium14),
                    SizedBox(height: 4),
                    Text(
                      'Starts From',
                      style: AppTypography.kLight12.copyWith(
                        color: AppColors.kNeutral04.withOpacity(0.75),
                      ),
                    ),
                    SizedBox(height: 8),
                    Container(
                      padding: EdgeInsets.symmetric(
                        vertical: 4.5,
                        horizontal: 8,
                      ),
                      decoration: BoxDecoration(
                        color: AppColors.kLime,
                        borderRadius: BorderRadius.circular(5),
                      ),
                      child: Text(
                        '\$ ${service.price.toInt()}',
                        style: AppTypography.kMedium12,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
