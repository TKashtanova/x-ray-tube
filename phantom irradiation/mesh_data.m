% Merging and post-processing of dose deposition .txt files obtained in Geant4
% by Tatiana Kashtanova
% 12/2023

clear;
clc;

% Inputs
% Simulation histories
tube_hist = 1e11;
% Path to Geant4 data
path = strcat("D:/output/56 mm/143 kVp/col cu0.0225 with al0.7+none/col5");
% Files numbering
file = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"];

% Mesh dimensions
dim_x = 250;
dim_y = 20;
dim_z = 250;

% Central axis voxels/bins
s = 124;
e = 127;


%%
% Multiplication factor for photons
fid = fopen(strcat(path,"mf.txt"));
df = textscan(fid,'%d','Delimiter',' ');
mf = double(df{1});
fclose(fid);

%%
% Dose deposition in the full mesh and central axis
t1 = zeros(dim_y, dim_z, dim_x);
t2 = zeros(dim_y, dim_z, dim_x);

for i = 1:length(file)
    mesh_name = strcat("Mesh_", file(i));
    [t1_i,t2_i] = mesh_data(path, file(i), dim_x, dim_y, dim_z); 
    t1 = t1 + t1_i;
    t2 = t2 + t2_i;
end

% Central axis mesh 
mc_t1 = t1(:, s:e, s:e);
mc_t2 = t2(:, s:e, s:e);
% Mean dose deposited along the central axis
% (Division by 16 to get the average over 4x4=16 bins)
dc_t1 = sum(sum(mc_t1,2),3)./16;
dc_t2 = sum(sum(mc_t2,2),3)./16;
% Central axis dose rate
rate_t1 = rate_data(dc_t1, mf, tube_hist);
rate_t2 = rate_data(dc_t2, mf, tube_hist);

%%
% Error bars
v1 = reshape(mc_t1,[20,16]);
sd1 = std(v1,0,2);
rate_sd1 = rate_data(sd1, mf, tube_hist);
v2 = reshape(mc_t2,[20,16]);
sd2 = std(v2,0,2);
rate_sd2 = rate_data(sd2, mf, tube_hist);

%%
% Print dose rate
% 1 Tube
fprintf('\n 1 Tube \n')
rate1_c = (rate_t1(10) + rate_t1(11))/2;
sd1_c = (rate_sd1(10) + rate_sd1(11))/2;
disp(['Surface: ', num2str(round(rate_t1(1),1)), ' +- ', num2str(round(rate_sd1(1),1))]);
disp(['Center: ', num2str(round(rate1_c,1)), ' +- ', num2str(round(sd1_c,1))]);
disp(['Bottom: ', num2str(round(rate_t1(20),1)), ' +- ', num2str(round(rate_sd1(20),1))]);


% 2 Tubes
fprintf('\n 2 Tubes \n')
rate2_c = (rate_t2(10) + rate_t2(11))/2;
sd2_c = (rate_sd2(10) + rate_sd2(11))/2;
disp(['Surface: ', num2str(round(rate_t2(1),1)), ' +- ', num2str(round(rate_sd2(1),1))]);
disp(['Center: ', num2str(round(rate2_c,1)), ' +- ', num2str(round(sd2_c,1))]); 
disp(['Bottom: ', num2str(round(rate_t2(20),1)), ' +- ', num2str(round(rate_sd2(20),1))]);


%%
% Longitudinal dose profile in the central axis
xt = reshape((0.5:1:20),20,1);
figure();
plot(xt, rate_t1, '-o', 'MarkerSize', 2, 'linewidth', 1)
xlabel('Depth (mm)','fontsize',12,'fontweight','bold')
ylabel('Dose Rate (Gy/s)','fontsize',12,'fontweight','bold')
xticks(0:5:20)
xticklabels({'-10', '-5', '0', '5', '10'})
grid on

figure();
plot(xt, rate_t2, '-o', 'MarkerSize', 2, 'linewidth', 1)
xlabel('Depth (mm)','fontsize',12,'fontweight','bold')
ylabel('Dose Rate (Gy/s)','fontsize',12,'fontweight','bold')
xticks(0:5:20)
xticklabels({'0', '5', '10', '15', '20'})
grid on

%%
% Cross-beam data
tube = t1;

% Dose along z-axis (inline)
d_cross_x = zeros(dim_y, 250);
% Dose along x-axis (crossline)
d_cross_z = zeros(dim_y, 250);
i = 1;
while i <= dim_z
    m_cross_x = tube(:, i, s:e);
    d_cross_x(:,i) = sum(m_cross_x,3)./4;
    m_cross_z = tube(:, s:e, i);
    d_cross_z(:,i) = sum(m_cross_z,2)./4;
    i = i+1;
end

% Dose rate
r_cross_x = rate_data(d_cross_x, mf, tube_hist);
r_cross_z = rate_data(d_cross_z, mf, tube_hist);

% Plots 
fig_x = cross_beam_plot(r_cross_x, 'x_true', 'Inline axis (mm)', path);
fig_z = cross_beam_plot(r_cross_z, 'z_true', 'Crossline axis (mm)', path);


%%
% Functions

% Read the scoring mesh
function [Mesh1, Mesh] = mesh_data(path, name, dim_x, dim_y, dim_z)    
    % Open Geant4 data
    data_txt = strcat("dDep_", name, ".txt");
    fid = fopen(strcat(path,data_txt));
    % Record needed data from .txt as a matrix
    df = textscan(fid,'%d %d %d %f %f %f','HeaderLines',3,'Delimiter',',');
    %df = textscan(fid,'%d %d %d %f','Delimiter',',');
    x = df{1};
    y = df{2};
    z = df{3};
    d = df{4};
    fclose(fid);
    
    M = zeros(size(x,1),4);
    M(:,1) = x;
    M(:,2) = y;
    M(:,3) = z;
    M(:,4) = d;

    % Top Tube
    % y,z,x
    Mesh1 = zeros(dim_y,dim_z,dim_x);
    M_row = 1;
    for xx = 1:dim_x
        % y,z
        page = zeros(dim_y,dim_z);
        yy_i = dim_y;
        for yy = 1:dim_y
            row = zeros(1,dim_z);
            for zz = 1:dim_z
                row(:,zz) = M(M_row, 4);
                M_row = M_row + 1;
            end
            page(yy_i,:) = row;
            yy_i = yy_i - 1;
        end
        Mesh1(:,:,xx) = page;
    end

    % Bottom Tube
    Mesh2 = rot90(Mesh1,2);

    % Both Tubes
    Mesh = Mesh1 + Mesh2;
end

% Compute dose-rate
function Rate = rate_data(dose, MF, sim_hist)
    % Tube current in A
    I_tube = 0.63;
    % Electron charge in Coulomb (A*s)
    Q = 1.602*1e-19;
    % Number of electrons from 1 tube
    Ne = sim_hist*MF;
    % Dose Rate (Gy/s)
    formula = I_tube./(Ne*Q);
    Rate = dose.*formula;
end

% Plot cross-beam profiles
function fig = cross_beam_plot(r_cross, x_label)
    xt = 1:250;
    fig = figure();
    for j = [2,6,11,16,20]
        df = r_cross(j, :);
        plot(xt, df, 'DisplayName', strcat(string(j-0.5), " mm"))
        hold on
    end
    xlabel(x_label,'fontsize',12,'fontweight','bold')
    ylabel('Dose Rate (Gy/s)','fontsize',12,'fontweight','bold')
    xticks(0:50:250)
    xticklabels({'-25', '-15', '-5', '5', '15', '25'})
    grid on
    lgd = legend('Location', 'northeast');
    lgd.Title.String = 'Distance from top';
    lgd.Title.FontSize = 12;
    ax = gca;
    ax.FontSize = 14;
    ax.YAxis.Exponent = 0;
end




