// DetectorConstruction.cc
#include "DetectorConstruction.hh"


MyDetectorConstruction::MyDetectorConstruction()
{
  DefineMaterials();
}

MyDetectorConstruction::~MyDetectorConstruction()
{}

void MyDetectorConstruction::DefineMaterials()
{
  G4NistManager *nist = G4NistManager::Instance();
  matWorld = nist->FindOrBuildMaterial("G4_AIR");
  matColBody = nist->FindOrBuildMaterial("G4_W");
  matPhantom = nist->FindOrBuildMaterial("G4_WATER");
}

G4VPhysicalVolume *MyDetectorConstruction::Construct()
{
  // World
  // Material - Air
  solidWorld = new G4Box("solidWorld", 50.*mm, 100.*mm, 50.*mm);
  logicWorld = new G4LogicalVolume(solidWorld, matWorld,"logicWorld");
  // rotation, translation position, logical volume, name, mother logical volume, boolean operation, number of copies, check for overlaps 
  physWorld = new G4PVPlacement(0, G4ThreeVector(0., 0., 0.), logicWorld, "physWorld", 0, false, 0, true);


  //Collimator Body
  // Material - Tungsten
  solidColBody = new G4Box("solidColBody", 25.*mm, 1.*mm, 25.*mm);
  logicColBody = new G4LogicalVolume(solidColBody, matColBody,"logicColBody");
  physColBody = new G4PVPlacement(0, G4ThreeVector(0, -57.*mm, -10.*mm), logicColBody, "physColBody", logicWorld, false, 0, true);


  //Collimator Window
  // Material - Air
  G4RotationMatrix* rWindow = new G4RotationMatrix;
  rWindow->rotateX(90.*deg);
  // inner radius, outer radius, half height, starting angle (rad), angle (rad)
  solidColWindow = new G4Tubs("solidColWindow", 0, 2.5*mm, 1.*mm, 0, 2*pi);
  logicColWindow = new G4LogicalVolume(solidColWindow, matWorld,"logicColWindow");
  physColWindow = new G4PVPlacement(rWindow, G4ThreeVector(0, 0, 0), logicColWindow, "physColWindow", logicColBody, false, 0, true);

  //Phantom
  // Material - Water
  solidPhantom = new G4Box("solidPhantom", 25.*mm, 10.*mm, 25.*mm);
  logicPhantom = new G4LogicalVolume(solidPhantom, matPhantom,"logicPhantom");
  physPhantom = new G4PVPlacement(0, G4ThreeVector(0, -71.*mm, -10.*mm), logicPhantom, "physPhantom", logicWorld, false, 0, true);

  return physWorld;
}

void MyDetectorConstruction::ConstructSDandField()
{
}


