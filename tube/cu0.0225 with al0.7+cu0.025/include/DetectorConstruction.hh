// DetectorConstruction.hh
#ifndef DetectorConstruction_hh
#define DetectorConstruction_hh

#include "G4VUserDetectorConstruction.hh"
#include "G4Material.hh"
#include "G4LogicalVolume.hh"
#include "G4VPhysicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4Box.hh"
#include "G4Cons.hh"
#include "G4ThreeVector.hh"
#include "G4SystemOfUnits.hh"
#include "G4PhysicalConstants.hh"
#include "G4NistManager.hh"
#include "DetectorSensitive.hh"


class MyDetectorConstruction : public G4VUserDetectorConstruction
{
  public:
    MyDetectorConstruction();
    ~MyDetectorConstruction();

    virtual G4VPhysicalVolume *Construct();

  private:
    virtual void ConstructSDandField();

    G4Box *solidWorld, *solidTCase, *solidAnode, *solidFilter1, *solidFilter2, *solidTShield, *solidTWindow, *solidDetector, *solidFilter3;
    G4Cons *solidTExit;
    G4LogicalVolume *logicWorld, *logicTCase, *logicAnode, *logicFilter1, *logicFilter2, *logicTShield, *logicTWindow, *logicTExit, *logicDetector, *logicFilter3;
    G4VPhysicalVolume *physWorld, *physTCase, *physAnode, *physFilter1, *physFilter2, *physTShield, *physTWindow, *physTExit, *physDetector, *physFilter3;

    G4Material *matWorld, *matTCase, *matAnode, *matFilter1, *matFilter2, *matTShield, *matFilter3;
    void DefineMaterials();
};

#endif

