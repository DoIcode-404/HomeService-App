import 'package:client/model/category_model.dart';
import 'package:client/modules/categories/components/category_card.dart';
import 'package:client/modules/home/components/search_field.dart';
import 'package:client/modules/widgets/animations/grid_animation.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';

class AllCategories extends StatefulWidget {
  const AllCategories({super.key});

  @override
  State<AllCategories> createState() => _AllCategoriesState();
}

class _AllCategoriesState extends State<AllCategories> {
  final TextEditingController _searchController = TextEditingController();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(leading: const BackButton()),
      body: SingleChildScrollView(
        padding: EdgeInsets.symmetric(horizontal: 20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(height: 20),
            PrimaryContainer(
              child: SearchField(
                controller: _searchController,
                onSearchPress: () {},
              ),
            ),
            SizedBox(height: 16),
            CustomHeaderText(text: 'All Categories', fontSize: 18),
            SizedBox(height: 16),
            PrimaryContainer(
              child: GridView.builder(
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 3,
                  childAspectRatio: 73 / 90,
                  crossAxisSpacing: 30,
                  mainAxisSpacing: 5,
                ),
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: categories.length,
                itemBuilder: ((context, index) {
                  return GridAnimatorWidget(
                    child: CategoryCard(
                      category: categories[index],
                      isGridView: true,
                    ),
                  );
                }),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
