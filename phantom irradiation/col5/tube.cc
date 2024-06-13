#include "G4Types.hh"

#ifdef G4MULTITHREADED
#include "G4MTRunManager.hh"
#else
#include "G4RunManager.hh"
#endif

#include "DetectorConstruction.hh"
#include "PhysicsList.hh"
#include "ActionInitialization.hh"

#include "G4UImanager.hh"
#include "G4UIExecutive.hh"
#include "G4VisManager.hh"
#include "G4VisExecutive.hh"

#include "G4ScoringManager.hh"


int main(int argc,char** argv)
{
  G4UIExecutive* ui = nullptr;
  if (argc == 1) 
  {
    ui = new G4UIExecutive(argc, argv);
  }

 #ifdef G4MULTITHREADED
   G4MTRunManager *runManager = new G4MTRunManager;
   runManager->SetNumberOfThreads(48);
 #else
   G4RunManager *runManager = new G4RunManager;
 #endif


 G4ScoringManager *scManager = G4ScoringManager::GetScoringManager();
 scManager->SetVerboseLevel(1);


 runManager->SetUserInitialization(new MyDetectorConstruction());
 runManager->SetUserInitialization(new MyPhysicsList());
 runManager->SetUserInitialization(new MyActionInitialization());


 G4VisManager *visManager = new G4VisExecutive;
 visManager->Initialize();


 runManager->Initialize();
  

 G4UImanager *UImanager = G4UImanager::GetUIpointer();  
 if (ui)  
 {
   UImanager->ApplyCommand("/control/execute vis.mac");
   ui->SessionStart();
   delete ui;
 }
 else           
 { 
   G4String command = "/control/execute ";
   G4String fileName = argv[1];
   UImanager->ApplyCommand(command+fileName);
 }


 delete visManager;
 delete runManager;

 return 0;
}
