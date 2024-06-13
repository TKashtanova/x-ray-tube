// DetectorConstruction.hh
#ifndef DetectorConstruction_hh
#define DetectorConstruction_hh

#include "G4VUserDetectorConstruction.hh"
#include "G4Material.hh"
#include "G4LogicalVolume.hh"
#include "G4VPhysicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4Box.hh"
#include "G4Tubs.hh"
#include "G4ThreeVector.hh"
#include "G4SystemOfUnits.hh"
#include "G4PhysicalConstants.hh"
#include "G4NistManager.hh"


class MyDetectorConstruction : public G4VUserDetectorConstruction
{
  public:
    MyDetectorConstruction();
    ~MyDetectorConstruction();

    virtual G4VPhysicalVolume *Construct();

private:
    virtual void ConstructSDandField();

    G4Box *solidWorld, *solidColBody, *solidPhantom;
    G4Tubs *solidColWindow;
    G4LogicalVolume *logicWorld, *logicColBody, *logicColWindow, *logicPhantom;
    G4VPhysicalVolume *physWorld, *physColBody, *physColWindow, *physPhantom;

    G4Material *matWorld, *matColBody, *matPhantom;
    void DefineMaterials();
};

#endif

