import 'package:animations/animations.dart';
import 'package:client/data/constants/constants.dart';
import 'package:client/model/service_model.dart';
import 'package:client/modules/categories/services_detail_view.dart';
import 'package:flutter/material.dart';

class HomeServicesCard extends StatelessWidget {
  final ServicesModel service;
  const HomeServicesCard({required this.service, super.key});

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
          child: Column(
            children: [
              Container(
                width: 139,
                height: 164,
                padding: EdgeInsets.all(9),
                alignment: Alignment.topLeft,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(10),
                  image: DecorationImage(
                    image: AssetImage(service.image),
                    fit: BoxFit.cover,
                  ),
                ),
                child:
                    service.discount != null
                        ? Container(
                          padding: EdgeInsets.symmetric(
                            horizontal: 5,
                            vertical: 3,
                          ),
                          decoration: BoxDecoration(
                            color: Colors.red,
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(
                            service.discount!,
                            style: AppTypography.kMedium12.copyWith(
                              color: AppColors.kWhite,
                            ),
                          ),
                        )
                        : null,
              ),
              const Spacer(),
              Text(service.name, style: AppTypography.kMedium14),
            ],
          ),
        );
      },
    );
  }
}
