% 脚本功能：生成 EgoHands 数据集所有帧的 .png 掩码文件

% 加载所有视频的元数据
% 不指定任何条件，获取全部 48 个视频
videos = getMetaBy();

% 创建输出目录
output_dir = 'masks';
if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

% 遍历所有视频
num_videos = length(videos);
for v = 1:num_videos
    % 获取当前视频的元数据
    vid = videos(v);
    video_id = vid.video_id;  % 例如 'CARDS_COURTYARDS_B_S'
    labelled_frames = vid.labelled_frames;  % 标注帧信息
    num_frames = length(labelled_frames);  % 每个视频 100 帧
    
    % 显示进度
    fprintf('处理视频 %d/%d: %s\n', v, num_videos, video_id);
    
    % 遍历当前视频的所有帧
    for f = 1:num_frames
        % 获取帧编号
        frame_num = labelled_frames(f).frame_num;
        
        % 生成手部分割掩码（包含所有手部）
        hand_mask = getSegmentationMask(vid, f, 'all');
        
        % 构造输出文件名，与原始图像对应
        mask_filename = sprintf('%s/%s_frame_%04d.png', output_dir, video_id, frame_num);
        
        % 保存掩码为 .png 文件（二值掩码需乘以 255 转换为 0-255 范围）
        imwrite(hand_mask * 255, mask_filename);
    end
end

% 完成提示
fprintf('所有掩码生成完成！总计 %d 张掩码已保存到 %s\n', num_videos * 100, output_dir);