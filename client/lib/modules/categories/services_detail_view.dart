import 'package:client/data/constants/constants.dart';
import 'package:client/model/property_type.dart';
import 'package:client/model/service_model.dart';
import 'package:client/modules/categories/components/detail_image_header.dart';
import 'package:client/modules/categories/components/property_type_card.dart';
import 'package:client/modules/categories/components/quantity_card.dart';
import 'package:client/modules/categories/components/service_sheet.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';

class ServicesDetailView extends StatefulWidget {
  final ServicesModel services;
  const ServicesDetailView({required this.services, super.key});

  @override
  State<ServicesDetailView> createState() => _ServicesDetailViewState();
}

class _ServicesDetailViewState extends State<ServicesDetailView> {
  int _selectedProperty = 1;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        leading: const BackButton(),
      ),
      body: SizedBox(
        height: MediaQuery.of(context).size.height,
        child: Stack(
          children: [
            DetailImageHeader(service: widget.services),
            Positioned(
              top: 228,
              left: 20,
              right: 20,
              child: SingleChildScrollView(
                child: Column(
                  children: [
                    PrimaryContainer(
                      child: Column(
                        children: [
                          CustomHeaderText(
                            text: 'Type of Property',
                            fontSize: 18,
                          ),
                          SizedBox(height: 16),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceAround,
                            children: List.generate(
                              3,
                              (index) => PropertyTypeCard(
                                property: properties[index],
                                onTap: () {
                                  setState(() {
                                    _selectedProperty = index;
                                  });
                                },
                                isSelected: _selectedProperty == index,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    SizedBox(height: 16),
                    PrimaryContainer(
                      child: Column(
                        children: [
                          QuantityCard(
                            text: 'Number of Units',
                            onChanged: (value) {},
                          ),
                          const Divider(),
                          QuantityCard(
                            text: 'Number of Bedrooms',
                            onChanged: (value) {},
                          ),
                        ],
                      ),
                    ),
                    SizedBox(height: 16),
                    PrimaryContainer(
                      child: Column(
                        children: [
                          CustomHeaderText(text: 'Description', fontSize: 18),
                          SizedBox(height: 16),
                          Text(
                            loremIpsumText,
                            style: AppTypography.kExtraLight13,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
      bottomSheet: ServiceSheet(
        bookText: 'Book Now',
        bookCallback: () {},
        isDetailPage: true,
        saveCallback: () {},
      ),
    );
  }
}
