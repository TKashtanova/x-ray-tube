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
  matTCase = nist->FindOrBuildMaterial("G4_Galactic");
  matAnode = nist->FindOrBuildMaterial("G4_W");
  matFilter1 = nist->FindOrBuildMaterial("G4_Cu");
  matFilter2 = nist->FindOrBuildMaterial("G4_Al");
  matTShield = nist->FindOrBuildMaterial("G4_Pb");
  matFilter3 = nist->FindOrBuildMaterial("G4_Cu");
}

G4VPhysicalVolume *MyDetectorConstruction::Construct()
{
  // World
  // Material - Air
  solidWorld = new G4Box("solidWorld", 300.*mm, 300.*mm, 300.*mm);
  logicWorld = new G4LogicalVolume(solidWorld, matWorld, "logicWorld");
  // rotation, translation position, logical volume, name, mother logical volume, boolean operation, number of copies, check for overlaps 
  physWorld = new G4PVPlacement(0, G4ThreeVector(0., 0., 0.), logicWorld, "physWorld", 0, false, 0, true);


  // Filter 1 (Inherent)
  // Material - Cu
  G4double f1 = 0.01125*mm;
  G4double f1_pos = -32.68875*mm;
  solidFilter1 = new G4Box("solidFilter1", 50.*mm, f1, 50.*mm);
  logicFilter1 = new G4LogicalVolume(solidFilter1, matFilter1, "logicFilter1");
  physFilter1 = new G4PVPlacement(0, G4ThreeVector(0, f1_pos, 0), logicFilter1, "physFilter1", logicWorld, false, 0, true);


  // Filter 2 (Inherent)
  // Material - Al
  G4double f2 = 0.35*mm;
  G4double f2_pos = -33.05*mm;
  solidFilter2 = new G4Box("solidFilter2", 50.*mm, f2, 50.*mm);
  logicFilter2 = new G4LogicalVolume(solidFilter2, matFilter2, "logicFilter2");
  physFilter2 = new G4PVPlacement(0, G4ThreeVector(0, f2_pos, 0), logicFilter2, "physFilter2", logicWorld, false, 0, true);

      
  // Tube Case
  // Material - Vacuum
  G4double tc = 32.6775*mm;
  solidTCase = new G4Box("solidTCase", 50.*mm, tc, 50.*mm);
  logicTCase = new G4LogicalVolume(solidTCase, matTCase, "logicTCase");
  physTCase = new G4PVPlacement(0, G4ThreeVector(0., 0., 0.), logicTCase, "physTCase", logicWorld, false, 0, true);    


  // Anode
  // Material - Tungsten
  G4RotationMatrix* rAnode = new G4RotationMatrix;
  rAnode->rotateX(74.*deg);
  solidAnode = new G4Box("solidAnode", 5.*mm, 2.*mm, 5.*mm);
  logicAnode = new G4LogicalVolume(solidAnode, matAnode,"logicAnode");
  physAnode = new G4PVPlacement(rAnode, G4ThreeVector(0., 0., -12.08*mm), logicAnode, "physAnode", logicTCase, false, 0, true); 

  G4Region* aRegion = new G4Region("anode");
  aRegion->AddRootLogicalVolume(logicAnode);


  //Tube Shielding
  // Material - Lead
  solidTShield = new G4Box("solidTShield", 50.*mm, 11.3*mm, 50.*mm);
  logicTShield = new G4LogicalVolume(solidTShield, matTShield,"logicTShield");
  physTShield = new G4PVPlacement(0, G4ThreeVector(0, -44.7*mm, 0), logicTShield, "physTShield", logicWorld, false, 0, true);


  //Tube Window
  // Material - Air
  solidTWindow = new G4Box("solidTWindow", 11.*mm, 1.9*mm, 11.*mm);
  logicTWindow = new G4LogicalVolume(solidTWindow, matWorld,"logicTWindow");
  physTWindow = new G4PVPlacement(0, G4ThreeVector(0, 9.4*mm, -10.*mm), logicTWindow, "physTWindow", logicTShield, false, 0, true);


  //Tube Exit
  // Material - Air
  G4RotationMatrix* rExit = new G4RotationMatrix;
  rExit->rotateX(-90.*deg);
  // inside radius 1, outside radius 1, inside radius 2, outside radius 2, half height, starting angle (rad), angle (rad)  
  solidTExit = new G4Cons("solidTExit", 0, 17.25*mm, 0, 24.*mm, 9.4*mm, 0, 2*pi);
  logicTExit = new G4LogicalVolume(solidTExit, matWorld,"logicTExit");
  physTExit = new G4PVPlacement(rExit, G4ThreeVector(0, -1.9*mm, -10.*mm), logicTExit, "physTExit", logicTShield, false, 0, true);


  // Filter 3 (External)
  // Material - Copper
  G4RotationMatrix* rFilter3 = new G4RotationMatrix;
  rFilter3->rotateX(-90.*deg);
  G4double f3_thk = 0.0125*mm;
  solidFilter3 = new G4Box("solidFilter3", 11.66*mm, f3_thk, 11.66*mm);
  logicFilter3 = new G4LogicalVolume(solidFilter3, matFilter3, "logicFilter3");
  physFilter3 = new G4PVPlacement(rFilter3, G4ThreeVector(0, 0, -9.4*mm+f3_thk), logicFilter3, "physFilter3", logicTExit, false, 0, true);


  // Sensitive Detector
  // Material - Air
  G4RotationMatrix* r_sd = new G4RotationMatrix;
  solidDetector = new G4Box("solidDetector", 25.*mm, 0.5*mm, 25.*mm);
  logicDetector = new G4LogicalVolume(solidDetector, matWorld, "logicDetector");
  physDetector = new G4PVPlacement(0, G4ThreeVector(0, -56.5*mm, -10.*mm), logicDetector, "physDetector", logicWorld, false, 0, true);  


  return physWorld;
}

void MyDetectorConstruction::ConstructSDandField()
{
    MySensitiveDetector *sensDet = new MySensitiveDetector("SensitiveDetector");
    logicDetector->SetSensitiveDetector(sensDet);
}
